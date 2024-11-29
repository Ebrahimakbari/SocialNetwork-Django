from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm,LoginForm
from django.contrib import messages

User = get_user_model()


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
    

class LoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    
    def get(self,request,*args, **kwargs):
        form = self.form_class()
        return render(request,self.template_name,context={'form':form})

    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password1', None)
            email = form.cleaned_data.get('email', None)
            user = User.objects.filter(email=email).first()
            if user.check_password(password):
                login(request,user)
                messages.success(request,'user successfully login')
                return redirect('home:home')
            messages.error(request,'incorrect password!!')
        
        return render(request,self.template_name,context={'form':form})
    

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'logout successfully!')
            return redirect('accounts:user_login')
