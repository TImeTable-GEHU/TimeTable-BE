from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    TEACHER_TYPES = [
        ("admin", "Admin"),
        ("hod", "HOD"),
        ("faculty", "Faculty"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Linked to User
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    working_days = models.CharField(max_length=100)
    teacher_code = models.CharField(max_length=10, unique=True, null=False)
    teacher_type = models.CharField(
        max_length=10, choices=TEACHER_TYPES, default="faculty"
    )

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.teacher_code}) - {self.department}"

    def delete(self, *args, **kwargs):
        """Ensure the corresponding user is deleted when the teacher is deleted."""
        user = self.user  # Store the user reference
        super().delete(*args, **kwargs)  # Delete the teacher
        user.delete()  # Manually delete the user

    @staticmethod
    def generate_teacher_code(name):
        """Generate a unique teacher_code"""
        initials = "".join([part[0].upper() for part in name.split() if part])
        existing_codes = Teacher.objects.filter(
            teacher_code__startswith=initials
        ).values_list("teacher_code", flat=True)
        existing_numbers = sorted(
            [
                int(code[len(initials) :])
                for code in existing_codes
                if code[len(initials) :].isdigit()
            ]
        )

        next_number = (existing_numbers[-1] + 1) if existing_numbers else 1
        return f"{initials}{next_number:03}"


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=10)
    semester = models.IntegerField()
    credits = models.IntegerField()
    dept = models.CharField(max_length=50)
    course = models.CharField(max_length=100)
    branch = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code}) - {self.dept} {self.semester} sem"


class TeacherSubject(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher_id.user.get_full_name()} teaches {self.subject_id.subject_name}"


class Room(models.Model):
    room_code = models.CharField(max_length=10)
    capacity = models.IntegerField()
    room_type = models.CharField(
        max_length=20,
        choices=(
            ("Class Room", "Class Room"),
            ("Lecture Theatre", "Lecture Theatre"),
            ("Lab", "Lab"),
            ("Seminar Hall", "Seminar Hall"),
        ),
        default="Class Room",
    )

    def __str__(self):
        return f"{self.room_code} ({self.room_type})"


class Student(models.Model):
    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=15)
    is_hosteller = models.BooleanField(default=False)
    location = models.CharField(max_length=100)
    dept = models.CharField(max_length=50)
    course = models.CharField(max_length=100)
    branch = models.CharField(max_length=100, default="")
    semester = models.IntegerField()
    section = models.CharField(max_length=2)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.student_name} ({self.student_id}) - Section {self.section}"
