from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random
# Create your models here.

# create random string for student code
def random_string(str_len=10):
    """Returns a random string of length string_length"""
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-","")
    return random[0:str_len]

class Student(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=18)
    student_code = models.CharField(max_length=100)
    student_grade = random_string(6)
    master_class = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    def __str__(self):
        return self.name

    class Meta:
        db_table = "tbl_student_account"

class User(AbstractUser):
    # Delete not use field
    username = None
    last_login = None
    is_staff = None
    is_superuser = None

    student_information = models.ForeignKey(Student, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = "tbl_user"