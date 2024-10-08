from django.contrib import admin
from .models import (User, 
                     UserProfile, 
                     PreferredContact, 
                     Agent, 
                     Customer,
                     Appointment,
                     Status,
                     TimeChoices,
                     AgentCancelledAppointment)

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(PreferredContact)
admin.site.register(TimeChoices)
admin.site.register(Agent)
admin.site.register(Customer)
admin.site.register(Appointment)
admin.site.register(Status)
admin.site.register(AgentCancelledAppointment)
