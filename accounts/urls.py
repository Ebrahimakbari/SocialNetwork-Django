from django.urls import path
from . import views


app_name= 'accounts'
urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='user_register'),
    path('login/',views.LoginView.as_view(),name='user_login'),
    path('logout/',views.LogoutView.as_view(),name='user_logout'),
    path('user-panel/<int:pk>/',views.UserPanelView.as_view(),name='user_panel'),
    path('change-password/<str:token>/',views.ChangePasswordView.as_view(),name='change_password'),
    path('reset-password-page/',views.ResetPasswordView.as_view(),name='reset_password'),
]
