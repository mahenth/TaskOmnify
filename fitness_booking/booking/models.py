from django.db import models

class FitnessClass(models.Model):
    """
    Model representing a fitness class offered by the studio.

    Fields:
        - name: Name of the fitness class (e.g., Yoga, Zumba).
        - datetime: Date and time when the class will be held.
        - instructor: Name of the instructor conducting the class.
        - available_slots: Number of available spots left for booking.
    """
    name = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        """
        String representation of the FitnessClass model,
        showing the class name and scheduled datetime.
        """
        return f"{self.name} - {self.datetime}"


class Booking(models.Model):
    """
    Model representing a booking made by a client for a fitness class.

    Fields:
        - fitness_class: ForeignKey linking to the booked FitnessClass.
        - client_name: Name of the client who made the booking.
        - client_email: Email of the client for communication.
    """
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()

    def __str__(self):
        """
        String representation of the Booking model,
        showing the client name and the booked fitness class name.
        """
        return f"{self.client_name} - {self.fitness_class.name}"
