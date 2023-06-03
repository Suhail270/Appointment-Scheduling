from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# For all users including customers and agents

class User(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    mobile = models.CharField(max_length=30)

# For organizations only (Motors, Real Estate, Fitness)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class BookingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class PreferredContact(models.Model):
    choice = models.CharField(max_length=100)

    objects = BookingManager()

    def __str__(self):
        return f"{self.choice}"
    
class TimeChoices(models.Model):

    # Format for time slots: 10:00 AM - 10:30 AM, 19 characters.
    
    choice = models.CharField(max_length=19)

    objects = BookingManager()

    def __str__(self):
        return f"{self.choice}"
    
class Status(models.Model):
    choice = models.CharField(max_length=100)

    objects = BookingManager()

    def __str__(self):
        return f"{self.choice}"

class Agent(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.email
    
    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.email
    
    def delete(self, *args, **kwargs):
        user = self.user
        user_profile = self.user.userprofile
        super().delete(*args, **kwargs)
        user.delete()
        user_profile.delete()

def get_default_status():
    return Status.objects.get_or_create(choice="Pending")[0]

class Appointment(models.Model):

    customer = models.ForeignKey("Customer", null=False, blank=False, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=False, blank=False, on_delete=models.CASCADE)
    day = models.DateField(null=False, blank=False)
    
    # Format for time slots: 10:00 AM - 10:30 AM, 19 characters.

    time = models.ForeignKey("TimeChoices", null=False, blank=False, on_delete=models.CASCADE)
    preferred_contact_method = models.ForeignKey("PreferredContact", null=False, blank=False, on_delete=models.CASCADE)
    status = models.ForeignKey("Status", null=False, blank=False, default=get_default_status, on_delete=models.CASCADE)

    organization = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Agent " + str(self.agent.user) + " - " + str(self.customer.user)
        
    
class AgentCancelledAppointment(models.Model):
    appointment = models.ForeignKey("Appointment", null=True, blank=True, on_delete=models.SET_NULL)
    reason = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return "Agent " + str(self.appointment.agent) + " - " + str(self.appointment.customer)


