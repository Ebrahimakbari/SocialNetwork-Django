from typing import Any
from django.conf import settings
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm,LoginForm,UserPanelFormChange,ResetPasswordForm,ChangePasswordForm,ForgetPasswordForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin,AccessMixin
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .models import Relation

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
    
    
class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'logout successfully!')
            return redirect('accounts:user_login')


class UserPanelView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        to_user = get_object_or_404(User, pk=user_id)
        is_follow = Relation.objects.filter(to_user=to_user, from_user=request.user).exists()
        posts = to_user.posts.all()
        if request.user != to_user:
            return render(request,'accounts/user_panel_read.html',{'posts':posts, 'is_follow':is_follow, "to_user":to_user})
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,*args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.prefetch_related('posts').get(id=user_id)
        followers = user.follower.all()
        followings = user.followings.all()
        form = UserPanelFormChange(instance=user)
        posts = user.posts.all()
        return render(request,'accounts/user_panel.html',{'form':form,'posts':posts,'followings':followings,'followers':followers})
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)
        form = UserPanelFormChange(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('home:home')
        messages.error(request,'invalid data')
        return render(request,'accounts/user_panel.html',{'form':form})


# send_mail(
#     "Subject here",
#     "Here is the message.",
#     "from@example.com",
#     ["to@example.com"],
#     fail_silently=False,
# )

class ResetPasswordView(View):
    def setup(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.user_form = ResetPasswordForm
        else:
            self.user_form = ForgetPasswordForm
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.user_form()
        return render(request, "accounts/reset_password.html", context={'form':form})
        
    def post(self, request, *args, **kwargs):
        form = self.user_form(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email', None)
            user = User.objects.get(email=user_email)
            user.token = get_random_string(length=32)
            user.save()
            try:
                send_mail('password reset link',
                        f"""click on this
                        http://{request.META['HTTP_HOST']}/accounts/change-password/{user.pk}/{user.token}/
                        link to redirect to pass reset page""",
                        settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[f"{user.email}"],
                        fail_silently=False,)
                messages.success(request, 'check your email box to reset ur password!')
            except:
                messages.error(request, "failed to send link to ur email!!!")
            return redirect('home:home')
        return render(request, "accounts/reset_password.html", context={'form':form})
    


class ChangePasswordView(View):
    def setup(self, request, *args, **kwargs):
        self.user_pk = kwargs.get('pk', None)
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        token = kwargs.get('token', None)
        user_token = User.objects.get(pk=self.user_pk).token
        if user_token != token:
            messages.error(request, 'invalid token!!')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        return render(request, "accounts/change_password.html", context={'form':form})
    
    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=self.user_pk)
            n_password = form.cleaned_data.get('password1', None)
            if n_password:
                user.set_password(n_password)
                user.save()
                messages.success(request,'new password successfully set!')
                return redirect('home:home')
        return render(request, "accounts/change_password.html", context={'form':form})