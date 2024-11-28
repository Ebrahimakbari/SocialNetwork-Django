from typing import Any
from django import forms
from django.contrib.auth.models import User


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
    
    # def clean_password2(self):
    #     password1 = self.cleaned_data['password1']
    #     password2 = self.cleaned_data['password2']
    #     if password1 != password2:
    #         raise forms.ValidationError('passwords not equal!!!')
    #     return password1
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password2 != password1:
            raise forms.ValidationError('mismatch password!!')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).exists()
        if user:
            raise forms.ValidationError('email already exists!!')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).exists()
        if user:
            raise forms.ValidationError('username already exists!!')
        return username