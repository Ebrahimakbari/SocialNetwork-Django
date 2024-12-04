from django.contrib import admin
from .models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserModel(admin.ModelAdmin):
    list_display = ['username','email','is_staff','is_superuser','last_login']