from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib import messages




class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    
    def get(self,request,*args, **kwargs):
        form = self.form_class()
        return render(request,self.template_name,context={'form':form})
    
    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get
            User.objects.create_user(data('username'),data('email'),data('password1'))        
            messages.success(request,'user successfully created')
            return redirect('home:home')

        return render(request,self.template_name,context={'form':form})