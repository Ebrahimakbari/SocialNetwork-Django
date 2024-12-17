from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username',
                            widget=forms.TextInput(attrs={
                                'class':'form-control', 
                                'placeholder':'username'
                                }))
    email = forms.EmailField(label='Email',
                            widget=forms.EmailInput(attrs={
                                'class':'form-control',
                                'placeholder':'email'
                                }))
    password1 = forms.CharField(label='Password',
                            widget=forms.PasswordInput(attrs={
                                'class':'form-control', 
                                'placeholder':'password'
                                }))
    password2 = forms.CharField(label='Confirm Password',
                            widget=forms.PasswordInput(attrs={
                                'class':'form-control', 
                                'placeholder':'confirm password'
                                }))
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1', None)
        password2 = cleaned_data.get('password2', None)
        if password1 and password2 and password2 != password1:
            raise ValidationError('mismatch password!!')
    
    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('email already exists!!')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('username already exists!!')
        return username
    

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',
                            widget=forms.EmailInput(attrs={
                                'class':'form-control',
                                'placeholder':'email'
                                }))
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={
                                'class':'form-control', 
                                'placeholder':'password'
                                }))
    
    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        user = User.objects.filter(email=email).exists()
        if not user:
            raise ValidationError('incorrect email or need register first!')
        return email
    

class UserPanelFormChange(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number','avatar']


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="Email",
                            widget=forms.EmailInput(attrs={
        "class":"form-control",
        "placeholder":"Email"
    }))
    password = forms.CharField(label="Password",
                            widget=forms.PasswordInput(attrs={
        "class":"form-control",
        "placeholder":"password"
    }))
    
    
    def clean(self):
        clean_data = super().clean()
        email = clean_data.get('email',None)
        password = clean_data.get('password',None)
        user = User.objects.filter(email=email)
        if not (
            email and
            password and
            user.exists and
            user.first().check_password(password)
            ):
            raise ValidationError('invalid pass or email!!')


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(label="Email",
                            widget=forms.EmailInput(attrs={
        "class":"form-control",
        "placeholder":"Email"
    }))
    
    def clean(self):
        clean_data = super().clean()
        email = clean_data.get('email',None)
        user = User.objects.filter(email=email)
        if not (
            email and
            user.exists
            ):
            raise ValidationError('invalid pass or email!!')


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='Password',
                            widget=forms.PasswordInput(attrs={
                                'class':'form-control', 
                                'placeholder':'password'
                                }))
    password2 = forms.CharField(label='Confirm Password',
                            widget=forms.PasswordInput(attrs={
                                'class':'form-control', 
                                'placeholder':'confirm password'
                                }))
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1', None)
        password2 = cleaned_data.get('password2', None)
        if password1 and password2 and password2 != password1:
            raise ValidationError('mismatch password!!')