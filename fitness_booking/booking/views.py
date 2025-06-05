from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer


class FitnessClassListAPIView(generics.ListAPIView):
    """
    API endpoint to list all upcoming fitness classes.

    Method: GET
    URL: /classes/

    Returns:
        - List of fitness classes ordered by upcoming date & time.
        - Each item includes class name, datetime, instructor, and available slots.
    """
    queryset = FitnessClass.objects.all().order_by('datetime')
    serializer_class = FitnessClassSerializer


class BookingCreateAPIView(generics.CreateAPIView):
    """
    API endpoint to create a new class booking.

    Method: POST
    URL: /book/
    Request Body:
        - fitness_class (int): ID of the fitness class
        - client_name (str)
        - client_email (str)

    Behavior:
        - Validates if the class has available slots.
        - If valid, creates booking and decrements slot count.
        - If full, returns 400 Bad Request with an error message.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingListByEmailAPIView(generics.ListAPIView):
    """
    API endpoint to retrieve all bookings made by a specific email.

    Method: GET
    URL: /bookings/?email=user@example.com

    Query Parameters:
        - email (str): Email address to filter bookings

    Returns:
        - List of bookings associated with the provided email.
    Raises:
        - ValidationError if 'email' query parameter is missing.
    """
    serializer_class = BookingSerializer

    def get_queryset(self):
        """
        Filter bookings based on the client's email provided in query params.
        """
        email = self.request.query_params.get('email')
        if not email:
            raise ValidationError("Query parameter 'email' is required.")
        return Booking.objects.filter(client_email=email)
