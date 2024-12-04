from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('detail/<int:pk>',views.PostDetailView.as_view(),name='post_detail'),
]
