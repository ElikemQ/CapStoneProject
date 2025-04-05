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
    

MEMBERSHIP_CHOICES = [
    ('daily', 'Daily'),
    ('monthly', 'Monthly'),
    ('quarterly', 'Quarterly'),
    ('bi-quarterly', 'Bi-Quarterly'),
    ('annualy', 'Annualy'),]

#membership model 
class Membership(models.Model):    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='membership')
    start_date = models.DateField()
    end_date = models.DateField()
    membership_type = models.CharField(max_length=25, choices=MEMBERSHIP_CHOICES)

    def __str__(self):
        return f'{self.user.username} - {self.membership_type} membership'
    
#roles model
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


PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('momo', 'Momo'),
        ('other', 'Other'),
    ]   

# payments model
class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)

    def __str__(self):
        return f'Your payment of {self.amount} by {self.user.username} for {self.membership.membership_type} membership' 


#announcements model
class Anouncements(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
#transactions model
class Transactions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='member_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20,choices=PAYMENT_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    

    class Meta:
        ordering = ['-payment_date']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f"{self.user.username} paid {self.amount} with {self.payment_method} on {self.payment_date.date()}"

