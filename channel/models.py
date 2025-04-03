from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


# Create your models here.

class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username
    

#types of memberships 


#membership model 
class Membership(models.Model):
    
    MEMBERSHIP_CHOICES = [
    ('daily', 'Daily'),
    ('monthly', 'Monthly'),
    ('quarterly', 'Quarterly'),
    ('bi-quarterly', 'Bi-Quarterly'),
    ('annualy', 'Annualy'),]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    start_date = models.DateField()
    end_date = models.DateField()
    membership_type = models.CharField(max_length=25, choices=MEMBERSHIP_CHOICES)

    def __str__(self):
        return f'{self.user.username} - {self.membership_type} Membership'
    

class Roles(models.Model):
    ROLES_CHOICES = [
        ('admin', 'Admin'),
        ('trainer', 'Trainer'),
        ('member', 'Member'),
    ]
    name = models.CharField(max_length=50, choices=ROLES_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='roles')

    def __str__(self):
        return self.name