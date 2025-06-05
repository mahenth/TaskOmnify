"# TaskOmnify" 
"# TaskOmnify" 
# Fitness Studio Booking API (Django + DRF)

A simple RESTful Booking API for a fictional fitness studio offering Yoga, Zumba, and HIIT classes.

---

## Features

- ✅ List all upcoming fitness classes
- ✅ Book a class by providing class ID, name, and email
- ✅ View bookings by email
- ✅ Slot availability validation
- ✅ Timezone support (Asia/Kolkata)
- ✅ Modular code using Class-Based Views (CBVs)
- ✅ SQLite database for simplicity

---

## Tech Stack

- Python 3.x
- Django 4.x
- Django REST Framework
- SQLite (default DB)
- Timezone: Asia/Kolkata

---

## Project Structure

fitness_booking/
├── booking/
│ ├── migrations/
│ ├── admin.py
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│ └── seed.py
├── fitness_booking/
│ ├── settings.py
│ ├── urls.py
├── db.sqlite3
├── manage.py
└── requirements.txt

2. Create Virtual Environment

python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Apply Migrations

python manage.py makemigrations
python manage.py migrate

5. Seed Initial Classes

python manage.py shell
>>> from booking.seed import run
>>> run()
>>> exit()

6. Run Development Server

python manage.py runserver
Server runs at: http://127.0.0.1:8000

API Endpoints (Test in Postman)
1. Get All Classes
GET /classes/


curl -X GET http://127.0.0.1:8000/classes/
2. Book a Class
POST /book/

{
  "fitness_class": 1,
  "client_name": "Mahenth",
  "client_email": "mahenth@example.com"
}

curl -X POST http://127.0.0.1:8000/book/ \
-H "Content-Type: application/json" \
-d '{"fitness_class":1, "client_name":"Mahenth", "client_email":"mahenth@example.com"}'

3. Get Bookings by Email
GET /bookings/?email=mahenth@example.com

curl -X GET http://127.0.0.1:8000/bookings/?email=mahenth@example.com


Evaluation Highlights
Area	            Covered ✅
Modular Code	    ✅ CBVs, serializers, utils
Input Validation	✅ Serializer checks
Slot Management	    ✅ Available slot decrement
Error Handling	    ✅ 400 on invalid requests
Timezone Support	✅ Asia/Kolkata
Clean API Design	✅ RESTful

Bonus	Includes seed data and curl samples

📦 Author & License
Created by Mahenth Vasudev