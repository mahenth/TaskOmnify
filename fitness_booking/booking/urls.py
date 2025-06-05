from django.urls import path
from .views import (
    FitnessClassListAPIView,
    BookingCreateAPIView,
    BookingListByEmailAPIView,
)

urlpatterns = [
    path('classes/', FitnessClassListAPIView.as_view(), name='classes-list'),
    path('book/', BookingCreateAPIView.as_view(), name='book-class'),
    path('bookings/', BookingListByEmailAPIView.as_view(), name='bookings-by-email'),
]
