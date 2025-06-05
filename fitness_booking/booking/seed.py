from .models import FitnessClass
from django.utils import timezone
from datetime import timedelta

def run():
    FitnessClass.objects.all().delete()
    FitnessClass.objects.create(name='Yoga', instructor='Anjali', datetime=timezone.now() + timedelta(days=1), available_slots=5)
    FitnessClass.objects.create(name='Zumba', instructor='Ravi', datetime=timezone.now() + timedelta(days=2), available_slots=3)
    FitnessClass.objects.create(name='HIIT', instructor='Sara', datetime=timezone.now() + timedelta(days=3), available_slots=2)
