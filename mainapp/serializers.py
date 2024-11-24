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
        fields = "__all__"  # Include all fields of Teacher model + preferred_subjects

    def get_preferred_subjects(self, obj):
        preferred_subjects = TeacherSubject.objects.filter(teacher_id=obj)
        return [ts.subject_id.subject_name for ts in preferred_subjects]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"
