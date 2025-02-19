from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from mainapp.models import Subject, Teacher, TeacherSubject
from mainapp.serializers import TeacherSerializer

from django.contrib.auth.models import User
from django.conf import settings

class TimetableSerializer(serializers.Serializer):
    course_id = serializers.CharField(max_length=100)
    semester = serializers.IntegerField()
    timetable = serializers.DictField()
    chromosome = serializers.CharField(max_length=255)
    last_updated = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_specific_teacher(request):
    """
    Retrieve the details of the authenticated teacher.
    """
    user = request.user
    teacher = Teacher.objects.filter(user=user).first()

    if not teacher:
        return Response({"error": "Teacher account not found."}, status=404)

    subject_codes = TeacherSubject.get_teacher_subjects(teacher.teacher_code)

    subject_names = list(
        Subject.objects.filter(subject_code__in=subject_codes).values_list(
            "subject_name", flat=True
        )
    )

    return Response(
        {
            "id": teacher.id,
            "name": user.get_full_name(),
            "email": user.email,
            "teacher_code": teacher.teacher_code,
            "teacher_type": teacher.teacher_type,
            "phone": teacher.phone,
            "department": teacher.department,
            "designation": teacher.designation,
            "working_days": teacher.working_days,
            "preferred_subjects": subject_names,
        },
        status=200,
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_teachers(request):
    """
    Retrieve a list of all teachers along with their preferred subjects.
    """
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def add_teacher(request):
    """
        Add a new teacher, generate a unique teacher_code & password,
        map preferred subjects in JSONField, and send credentials via email.
    """
    teacher_data = request.data

    email = teacher_data.get("email", "").strip().lower()
    full_name = teacher_data.get("name", "").strip()

    if not email or not full_name:
        return Response({"error": "Email and Name are required."}, status=400)

    existing_user = User.objects.filter(email=email).first()
    if existing_user:
        return Response({"error": "User with this email already exists."}, status=400)

    teacher_code = Teacher.generate_teacher_code(full_name)
    first_name = full_name.split()[0]
    raw_password = f"{first_name}{teacher_code}"

    # Create User and hash password automatically
    user = User.objects.create_user(
        username=teacher_code.lower(),
        email=email,
        first_name=full_name.split()[0],
        last_name=" ".join(full_name.split()[1:]),
        password=raw_password,
    )

    # Create the Teacher linked to User
    teacher = Teacher.objects.create(
        user=user,
        phone=teacher_data.get("phone", ""),
        department=teacher_data.get("department", ""),
        designation=teacher_data.get("designation", ""),
        working_days=teacher_data.get("working_days", ""),
        teacher_code=teacher_code,
        teacher_type=teacher_data.get("teacher_type", "faculty"),
    )

    subject_names = teacher_data.get("preferred_subjects", [])
    # Convert subject names to subject codes
    subject_codes = []
    for subject_name in subject_names:
        subject = Subject.objects.filter(subject_name=subject_name).first()
        if subject:
            subject_codes.append(subject.subject_code)
        else:
            return Response(
                {"error": f"Subject '{subject_name}' not found."}, status=404
            )

    # Map preferred subjects using subject codes
    for subject_code in subject_codes:
        TeacherSubject.add_teacher_to_subject(subject_code, teacher_code)

    # Send email with credentials
    email_subject = "Your Teacher Account Credentials"
    email_body = render_to_string(
        "emails/teacher_confirmation_email.html",
        {
            "teacher_name": full_name,
            "teacher_code": teacher_code,
            "preferred_subjects": subject_names,
            "email": email,
            "password": raw_password,
        },
    )

    try:
        send_mail(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
            html_message=email_body,
        )
    except Exception as e:
        return Response({"error": f"Failed to send email: {str(e)}"}, status=500)

    return Response(
        {"message": "Teacher added successfully, credentials sent via email."},
        status=201,
    )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_teacher(request, pk):
    """
    Update an existing teacher's details by ID, including preferred subjects.
    """
    try:
        teacher = Teacher.objects.get(id=pk)
        serializer = TeacherSerializer(
            instance=teacher, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()

            if "preferred_subjects" in request.data:
                new_subject_names = request.data["preferred_subjects"]
                teacher_code = teacher.teacher_code

                # Fetch existing mapping and remove teacher from all assigned subjects
                try:
                    mapping = TeacherSubject.objects.get(id=1)
                    for subject_code in list(mapping.subject_teacher_map.keys()):
                        if teacher_code in mapping.subject_teacher_map[subject_code]:
                            mapping.subject_teacher_map[subject_code].remove(
                                teacher_code
                            )
                            if not mapping.subject_teacher_map[
                                subject_code
                            ]:  # Remove key if empty
                                del mapping.subject_teacher_map[subject_code]
                    mapping.save()
                except TeacherSubject.DoesNotExist:
                    pass  # No mapping exists yet, so nothing to remove

                # Convert subject names to subject codes
                subject_codes = []
                for subject_name in new_subject_names:
                    subject = Subject.objects.filter(subject_name=subject_name).first()
                    if subject:
                        subject_codes.append(subject.subject_code)
                    else:
                        return Response(
                            {"error": f"Subject '{subject_name}' not found."},
                            status=404,
                        )

                # Add teacher to new preferred subjects
                for subject_code in subject_codes:
                    TeacherSubject.add_teacher_to_subject(subject_code, teacher_code)

            # Fetch updated subject names for response
            updated_subject_codes = TeacherSubject.get_teacher_subjects(
                teacher.teacher_code
            )
            updated_subject_names = [
                Subject.objects.get(subject_code=code).subject_name
                for code in updated_subject_codes
            ]

            return Response(
                {
                    "id": teacher.id,
                    "name": teacher.user.get_full_name(),
                    "email": teacher.user.email,
                    "teacher_code": teacher.teacher_code,
                    "phone": teacher.phone,
                    "department": teacher.department,
                    "designation": teacher.designation,
                    "working_days": teacher.working_days,
                    "preferred_subjects": updated_subject_names,
                },
                status=200,
            )
        else:
            return Response(serializer.errors, status=400)

    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=404)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_teacher(request, pk):
    """
    Delete a teacher by ID.
    """
    try:
        teacher = Teacher.objects.get(id=pk)
        teacher.delete()
        return Response({"message": "Teacher deleted successfully"}, status=200)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=404)
