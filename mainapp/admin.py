from django.contrib import admin
from .models import Room, Teacher, Subject, TeacherSubject, Student


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_code", "room_type", "capacity")
    search_fields = ("room_code", "room_type")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "department",
        "designation",
        "email",
        "phone",
        "working_days",
    )
    search_fields = ("name", "department", "email", "designation")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "subject_name",
        "subject_code",
        "semester",
        "credits",
        "dept",
        "course",
    )
    search_fields = ("subject_name", "subject_code", "dept", "course")


@admin.register(TeacherSubject)
class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = ("teacher_id", "subject_id")
    search_fields = ("teacher_id__name", "subject_id__subject_name")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_name",
        "student_id",
        "section",
        "semester",
        "dept",
        "course",
        "cgpa",
        "is_hosteller",
        "location",
    )
    search_fields = ("student_name", "student_id", "section", "dept", "course")
