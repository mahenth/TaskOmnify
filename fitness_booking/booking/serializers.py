from rest_framework import serializers
from .models import FitnessClass, Booking
from django.utils.timezone import localtime

class FitnessClassSerializer(serializers.ModelSerializer):
    datetime = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = '__all__'

    def get_datetime(self, obj):
        return localtime(obj.datetime).strftime("%Y-%m-%d %H:%M:%S")

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        cls = data['fitness_class']
        if cls.available_slots <= 0:
            raise serializers.ValidationError("No slots available.")
        return data

    def create(self, validated_data):
        cls = validated_data['fitness_class']
        cls.available_slots -= 1
        cls.save()
        return super().create(validated_data)
