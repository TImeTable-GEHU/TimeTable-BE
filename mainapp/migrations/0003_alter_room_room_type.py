# Generated by Django 5.1.3 on 2024-11-23 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0002_student_delete_section"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="room_type",
            field=models.CharField(
                choices=[
                    ("Class Room", "Class Room"),
                    ("Lecture Theatre", "Lecture Theatre"),
                    ("Lab", "Lab"),
                    ("Seminar Hall", "Seminar Hall"),
                ],
                default="Class Room",
                max_length=20,
            ),
        ),
    ]