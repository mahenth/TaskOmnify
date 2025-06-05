from rest_framework import generics
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from rest_framework.exceptions import ValidationError

class FitnessClassListAPIView(generics.ListAPIView):
    """GET /classes/"""
    queryset = FitnessClass.objects.all().order_by('datetime')
    serializer_class = FitnessClassSerializer


class BookingCreateAPIView(generics.CreateAPIView):
    """POST /book/"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingListByEmailAPIView(generics.ListAPIView):
    """GET /bookings/?email=user@example.com"""
    serializer_class = BookingSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        if not email:
            raise ValidationError("Query parameter 'email' is required.")
        return Booking.objects.filter(client_email=email)
