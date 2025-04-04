.venv\Scripts\activate // Khởi chạy môi trường ảo

- Chạy BE
  - .venv\Scripts\activate
  - python backend.py
- Chạy FE
  - .venv\Scripts\activate
  - cd frontend
  - node server.js

django-admin startproject tvdung // Bắt đầu project
cd tvdung_project01
python manage.py runserver // Chạy server

django-admin startapp customer // Tạo model mới

python manage.py makemigrations // Cập nhật cho db ứng với model
python manage.py migrate // Kết nối db hoặc cập nhật db
python manage.py createsuperuser //Tạo người dùng admin ten tvdung, pass 12345678

python manage.py migrate auth
python manage.py migrate users

Kiểm tra mạng trước khi chạy docker: npx http-server .
