from rest_framework import serializers
from .models import Room, Teacher, Subject, TeacherSubject


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    preferred_subjects = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = "__all__"
        read_only_fields = ["teacher_code"]

    def get_preferred_subjects(self, obj):
        preferred_subjects = TeacherSubject.objects.filter(teacher_id=obj)
        return [ts.subject_id.subject_name for ts in preferred_subjects]

    def create(self, validated_data):
        name = validated_data.get("name")
        initials = "".join([part[0].upper() for part in name.split() if part])
        next_number = Teacher.objects.count() + 1
        teacher_code = f"{initials}{next_number:03}"
        validated_data["teacher_code"] = teacher_code
        return super().create(validated_data)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"
