from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from students.serializers import StudentSerializers
from students.models import Student


# Create your views here.

# get, create and delete student
@api_view(['GET', 'POST', 'DELETE'])
def list_students(request):
    if request.method == "GET":
        list_student = Student.objects.all().order_by('id')[:28].reverse()
        print("list student: \n {}".format(list_student))
        name = request.GET.get('name', None)
        if name is not None:
            list_student = list_student.filter(name=name)
        student_serializers = StudentSerializers(list_student, many=True)
        # safe = False is for objects serializers
        return JsonResponse(student_serializers.data, safe=False)
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
    else:
        return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# get, edit and delete student profile
@api_view(['GET', 'PUT', 'DELETE'])
def profile(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return JsonResponse({"message": "This student does not exist!"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        student_serializers = StudentSerializers(student)
        return JsonResponse(student_serializers.data)
    elif request.method == "DELETE":
        student.delete()
        return JsonResponse({"message": "Delete student successfully!"}, status=status.HTTP_204_NO_CONTENT)
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
    students = Student.objects.filter(id__gt=0)[:28]
    if request.method == "GET":
        if students is not None:
            print("lst students: \n {}".format(students))
        student_serializers = StudentSerializers(students, many=True)
        return JsonResponse(student_serializers.data, safe=False)
    elif request.method == "DELETE":
        delete_all = Student.objects.all().delete()
        return JsonResponse({"message": "All {} students have been deleted".format(delete_all[0])})
    else:
        return JsonResponse({"message": "Method not allowed"})
