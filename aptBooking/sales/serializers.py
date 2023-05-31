from rest_framework import serializers
from sales.models import Appointment, User, Agent

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


class agentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = (
            'user',
            'organization'
        )

# class userSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fileds = (
#             ''
#         )