from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register([Profile, Stock, Category, Sales, History, Transaction])
