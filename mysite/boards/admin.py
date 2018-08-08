from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Board

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Board)
# Register your models here.
