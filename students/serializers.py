from rest_framework import serializers
from students.models import Student
from students.models import User

class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'name',
            'age',
            'student_grade',
            'master_class',
            'student_code',
            'description'
                )

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class UserLoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        email = serializers.EmailField(required=True)
        password = serializers.CharField(required=True)