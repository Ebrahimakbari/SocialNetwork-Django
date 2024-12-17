from django.contrib import admin
from .models import CustomUser,Relation
# Register your models here.


@admin.register(CustomUser)
class CustomUserModel(admin.ModelAdmin):
    list_display = ['username','email','is_staff','is_superuser','last_login']

@admin.register(Relation)
class CustomUserModel(admin.ModelAdmin):
    list_display = ['to_user', 'from_user', 'created']