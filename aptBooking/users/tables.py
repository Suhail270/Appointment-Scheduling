# tutorial/tables.py
import django_tables2 as tables
from sales.models import Appointment,AgentCancelledAppointment

class AppointmentTable(tables.Table):
    class Meta:
        model = Appointment
        template_name = "django_tables2/bootstrap.html"
        fields = (
            'customer_id',
            'agent_id',
            'day',
            'time_id',
            'preferred_contact_method_id',
            'status_id'
        )

class CancelledAppointmentTable(tables.Table):
    class Meta:
        model = AgentCancelledAppointment
        template_name = "django_tables2/bootstrap.html"
        fields = (
            'appointment',
            'reason'
        )