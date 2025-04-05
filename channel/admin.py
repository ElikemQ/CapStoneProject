from django.contrib import admin

# Register your models here.
from.models import Membership, Roles, Payments, Anouncements, Transactions,CustomUser

admin.site.register(Membership)
admin.site.register(Roles)
admin.site.register(Payments)
admin.site.register(Anouncements)
admin.site.register(Transactions)
admin.site.register(CustomUser)
