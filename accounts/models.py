from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser,PermissionsMixin
from .managers import CustomUserManager
# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(blank=True,unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    avatar = models.ImageField(upload_to='user/avatar', blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    token = models.CharField(max_length=100,null=True, blank=True)
    is_staff = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    
    def __str__(self) -> str:
        return self.email
    
    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")