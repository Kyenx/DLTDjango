from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Board, Topic

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Board)
admin.site.register(Topic)
# Register your models here.
