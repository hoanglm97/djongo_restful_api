from django.db import models


# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=18)
    student_grade = models.CharField(max_length=200)
    master_class = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
