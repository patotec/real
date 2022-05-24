from django.contrib import admin
from .models import *



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username',  'email']
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user',  'approve']





admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Pay_method)
admin.site.register(Request)
admin.site.register(Payment,PaymentAdmin)
