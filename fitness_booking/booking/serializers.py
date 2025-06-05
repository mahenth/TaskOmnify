from rest_framework import serializers
from django.utils.timezone import localtime
from .models import FitnessClass, Booking


class FitnessClassSerializer(serializers.ModelSerializer):
    """
    Serializer for the FitnessClass model.
    Formats the datetime field into a local time string.
    """
    datetime = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = '__all__'

    def get_datetime(self, obj):
        """
        Return the datetime in local time (IST by default) formatted as a string.
        Example: '2025-06-05 18:30:00'
        """
        return localtime(obj.datetime).strftime("%Y-%m-%d %H:%M:%S")


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    Handles validation and creation logic related to available class slots.
    """

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        """
        Check if there are available slots before allowing booking.
        Raises:
            ValidationError: If no slots are available for the selected class.
        """
        cls = data['fitness_class']
        if cls.available_slots <= 0:
            raise serializers.ValidationError("No slots available.")
        return data

    def create(self, validated_data):
        """
        Reduce available_slots by 1 when a booking is successfully created.
        """
        cls = validated_data['fitness_class']
        cls.available_slots -= 1
        cls.save()
        return super().create(validated_data)
