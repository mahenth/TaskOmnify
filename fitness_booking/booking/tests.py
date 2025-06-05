from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import FitnessClass, Booking
from datetime import timedelta


class BookingAPITestCase(APITestCase):

    def setUp(self):
        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            instructor="Anjali",
            datetime=timezone.now() + timedelta(days=1),
            available_slots=2
        )
        self.booking_url = "/book/"
        self.classes_url = "/classes/"
        self.bookings_url = "/bookings/"

    def test_list_classes(self):
        response = self.client.get(self.classes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_successful_booking(self):
        data = {
            "fitness_class": self.fitness_class.id,
            "client_name": "Mahenth",
            "client_email": "mahenth@example.com"
        }
        response = self.client.post(self.booking_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.fitness_class.refresh_from_db()
        self.assertEqual(self.fitness_class.available_slots, 1)

    def test_overbooking(self):
        # Book twice (slots = 2)
        for _ in range(2):
            self.client.post(self.booking_url, {
                "fitness_class": self.fitness_class.id,
                "client_name": "Client",
                "client_email": f"client{_}@test.com"
            }, format='json')

        # Third booking should fail
        response = self.client.post(self.booking_url, {
            "fitness_class": self.fitness_class.id,
            "client_name": "Client",
            "client_email": "client3@test.com"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No available slots", str(response.data))

    def test_get_bookings_by_email(self):
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="Test User",
            client_email="user@example.com"
        )

        response = self.client.get(f"{self.bookings_url}?email=user@example.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
