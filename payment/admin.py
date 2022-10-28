from django.contrib import admin
from .models import Number, Order, Transaction
# Register your models here.

admin.site.register(Number) 
admin.site.register(Order) 
admin.site.register(Transaction) 
