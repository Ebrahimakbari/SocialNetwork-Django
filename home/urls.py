from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('detail/<int:pk>/<slug:post_slug>/',views.PostDetailView.as_view(),name='post_detail'),
    path('edit/<int:pk>/<slug:post_slug>/',views.PostEditView.as_view(),name='post_edit'),
    path('create/',views.PostCreateView.as_view(),name='post_create'),
    path('delete/<int:pk>/',views.PostDeleteView.as_view(),name='post_delete'),
]
