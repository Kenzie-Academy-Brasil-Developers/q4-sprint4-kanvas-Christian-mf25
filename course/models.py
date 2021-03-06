from uuid import uuid4

from django.db import models

class Course(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	name = models.CharField(max_length=255, unique=True)
	demo_time = models.TimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	link_repo = models.CharField(max_length=255)
	instructor = models.OneToOneField("user.User", on_delete=models.CASCADE, related_name="instructor_course", null=True, blank=True)
	students = models.ManyToManyField("user.User", related_name="students_course")
