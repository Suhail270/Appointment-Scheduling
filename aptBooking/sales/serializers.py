from rest_framework import serializers
from sales.models import Appointment, User

class appointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            'customer_id',
            'agent_id',
            'day',
            'time_id',
            'preferred_contact_method_id',
            'status_id'
        )

# class userSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fileds = (
#             ''
#         )