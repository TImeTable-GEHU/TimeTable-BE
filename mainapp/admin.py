from django.contrib import admin

from .models import Room, Student, Subject, Teacher, TeacherSubject

admin.site.register(Room)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(TeacherSubject)
admin.site.register(Student)
