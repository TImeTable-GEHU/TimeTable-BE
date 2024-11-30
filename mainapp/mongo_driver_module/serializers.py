# serializers.py
from rest_framework import serializers

class TimetableSerializer(serializers.Serializer):
    course_id = serializers.CharField(max_length=100)
    semester = serializers.IntegerField()
    timetable = serializers.DictField()
    chromosome = serializers.CharField(max_length=255)
    last_updated = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
