# Django Restful CRUD(*) API with MongoDB example
- Yêu cầu để chạy bao gồm:
    - Python version: 3.x
    - Django version: 2.1++
    - MongoDb version: 3.4++ 
    - djongo version: 1.3.1++
    - django-cors-headers: 3.2.0++
    - Django Rest Framework: 3.11.0
```
# Coi như terminal đang ở vị trí của project này 
Tạo, active venv: 
    - virtualenv venv
    - source venv/bin/activate
Cài cái package cần thiết:
    - pip install -r requirements.txt
        + lưu ý trong quá trình cài có thể sẽ bị warning pip
            => vì vậy nên update pip lên bản mới nhất trước khi cài
                ví dụ, coi như đã active venv chạy lệnh sau: 
                    python3 -m pip install --upgrade pip 
Thay đổi db, host, port trong db:
    - tìm thư mục djongo_rest_api vào file settings.py và tìm dòng DATABASES = [...]
Tạo các collection trong db:
    - python3 manage.py migrate students
        + lưu ý nếu thay đổi field hoặc thêm nhiều fields thì vào students/models.py,
            sau đó chạy: python3 manage.py makemigrations students
        + sau khi thêm 1 hoặc nhiều fields thì cần thêm các fields đo vào trong serializers để dùng trong QuerySet
Để thêm url cho các api: students/urls.py
Để thêm api mới: students/views.py
Chạy server:
    - python3 manage.py runserver 8080 
        => mở URL: http://{yourhost}:8080/
            => ví dụ: http://localhost:8080/
Test api: có thể dùng Postman và allow all host cho port 8080 để test trên server.
```
#### (*) : CRUD => create read update delete
### Ansible deploy project incoming soon.