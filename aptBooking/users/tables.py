# tutorial/tables.py
import django_tables2 as tables
from sales.models import Appointment

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