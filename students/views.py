from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from students.serializers import StudentSerializers, UserLoginSerializer, UserSerializer
from students.models import Student, User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Create your views here.

# register user
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.validated_data['password'] = make_password(user_serializer.validated_data['password'])
            print("pwd: {}".format(user_serializer.validated_data['password']))
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# login via email and password
@api_view(["POST"])
def login_required(request):
    # if request.method == 'POST':
        # user_data = JSONParser().parse(request)
    user = UserLoginSerializer(data=request.data)
    if user.is_valid():
        print("something!")
        user = authenticate(
            request,
            username=user.validated_data['email'],
            password=user.validated_data['password']
        )
        print("user: {}".format(user))
        if user:
            refresh = TokenObtainPairSerializer.get_token(user)
            data = {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token)
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        return JsonResponse({
            'error_message': 'Email or password is incorrect!',
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({
        'error_messages': user.errors,
        'error_code': 400
    }, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# get, create and delete student
@api_view(['GET', 'POST', 'DELETE'])
def list_students(request):
    if request.method == "GET":
        # find all student in collection and order_by id 
        list_student = Student.objects.all().order_by('id')
        print("list student: \n {}".format(list_student))
        name = request.GET.get('name', None)
        if name is not None:
            list_student = list_student.filter(name=name)
        student_serializers = StudentSerializers(list_student, many=True)
        # safe = False is for objects serializers
        return JsonResponse(student_serializers.data, safe=False)
    # create student
    elif request.method == 'POST':
        student_data = JSONParser().parse(request)
        if student_data:
            print("Student data : {}".format(student_data))
        student_serializer = StudentSerializers(data=student_data)
        print('student_serializer: {}'.format(student_serializer))
        if student_serializer.is_valid():
            student_serializer.save()
            return JsonResponse(student_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # if method is not ["GET", "POST"] => throw error 405 HTTP
    else:
        return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# get, edit and delete student profile
@api_view(['GET', 'PUT', 'DELETE'])
def profile(request, pk):
    try:
        # get id student if not => response error 404 HTTP
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return JsonResponse({"message": "This student does not exist!"}, status=status.HTTP_404_NOT_FOUND)
    # get student by id
    if request.method == "GET":
        student_serializers = StudentSerializers(student)
        return JsonResponse(student_serializers.data)
    # delete student by id
    elif request.method == "DELETE":
        student.delete()
        return JsonResponse({"message": "Delete student successfully!"}, status=status.HTTP_204_NO_CONTENT)
    # edit student by id
    elif request.method == "PUT":
        student_data = JSONParser().parse(request)
        student_serializers = StudentSerializers(student, data=student_data)
        if student_serializers.is_valid():
            student_serializers.save()
            return JsonResponse(student_serializers.data)
        return JsonResponse(student_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# get all student in class
@api_view(["GET", "DELETE"])
def all_list_students(request):
    # filter by id greater than 0
    students = Student.objects.filter().order_by("id")
    if request.method == "GET":
        if students is not None:
            print("lst students: \n {}".format(students))
        student_serializers = StudentSerializers(students, many=True)
        return JsonResponse(student_serializers.data, safe=False)
    elif request.method == "DELETE":
        # find all students all delete all
        delete_all = Student.objects.all().delete()
        return JsonResponse({"message": "All {} students have been deleted".format(delete_all[0])})
    else:
        return JsonResponse({"message": "Method not allowed"})
