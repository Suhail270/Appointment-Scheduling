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
    choice = models.CharField(max_length=10)

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
        user_profile = self.user.userprofile
        super().delete(*args, **kwargs)
        user.delete()
        user_profile.delete()

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

class Appointment(models.Model):
    customer = models.ForeignKey("Customer", null=True, blank=True, on_delete=models.SET_NULL)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    day = models.DateField()
    time = models.ForeignKey("TimeChoices", null=True, blank=True, on_delete=models.SET_NULL)
    preferred_contact_method = models.ForeignKey("PreferredContact", null=True, blank=True, on_delete=models.SET_NULL)
    status = models.ForeignKey("Status", null=True, blank=True, on_delete=models.SET_NULL)

    


