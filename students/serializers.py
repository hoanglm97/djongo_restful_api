from rest_framework import serializers
from students.models import Student


class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('name',
                  'age',
                  'student_grade',
                  'master_class',
                  'description')
