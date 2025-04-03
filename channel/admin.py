from django.contrib import admin

# Register your models here.
from.models import Membership, Roles

admin.site.register(Membership)
admin.site.register(Roles)