from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import FitnessClass, Booking
from datetime import timedelta


class BookingAPITestCase(APITestCase):
    """
    Unit tests for the Booking API using Django REST Framework's APITestCase.
    Covers class listing, booking functionality, overbooking protection,
    and retrieving bookings by client email.
    """

    def setUp(self):
        """
        Set up a sample fitness class for testing purposes.
        This will be reused across multiple tests.
        """
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
        """
        Test that the /classes/ endpoint returns a list of available classes.
        """
        response = self.client.get(self.classes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn("name", response.data[0])  # Ensure fields are present

    def test_successful_booking(self):
        """
        Test that a class can be successfully booked and
        available slots decrease by 1.
        """
        data = {
            "fitness_class": self.fitness_class.id,
            "client_name": "Mahenth",
            "client_email": "mahenth@example.com"
        }
        response = self.client.post(self.booking_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Refresh class from DB and check slot count
        self.fitness_class.refresh_from_db()
        self.assertEqual(self.fitness_class.available_slots, 1)

    def test_overbooking(self):
        """
        Test that trying to book more than the available slots fails.
        """
        # Book all available slots (2 bookings)
        for i in range(2):
            self.client.post(self.booking_url, {
                "fitness_class": self.fitness_class.id,
                "client_name": f"Client {i}",
                "client_email": f"client{i}@test.com"
            }, format='json')

        # Attempt to overbook (3rd booking)
        response = self.client.post(self.booking_url, {
            "fitness_class": self.fitness_class.id,
            "client_name": "Client 3",
            "client_email": "client3@test.com"
        }, format='json')

        # Ensure overbooking is not allowed
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No slots available.", response.data.get('non_field_errors')[0])

    def test_get_bookings_by_email(self):
        """
        Test retrieving bookings using the /bookings/?email= endpoint.
        """
        # Create a booking
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="Test User",
            client_email="user@example.com"
        )

        # Fetch bookings for the email
        response = self.client.get(f"{self.bookings_url}?email=user@example.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["client_email"], "user@example.com")
