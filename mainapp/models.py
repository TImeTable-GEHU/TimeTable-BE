from django.db import models


class Teacher(models.Model):
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    working_days = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.designation}, {self.department})"


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=10)
    semester = models.IntegerField()
    credits = models.IntegerField()
    dept = models.CharField(max_length=50)
    course = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code}) - {self.dept} {self.semester} sem"


class TeacherSubject(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher_id.name} teaches {self.subject_id.subject_name}"


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
    semester = models.IntegerField()
    section = models.CharField(max_length=2)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.student_name} ({self.student_id}) - Section {self.section}"
