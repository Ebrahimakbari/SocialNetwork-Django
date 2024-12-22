from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('detail/<int:pk>/<slug:post_slug>/',views.PostDetailView.as_view(),name='post_detail'),
    path('edit/<int:pk>/<slug:post_slug>/',views.PostEditView.as_view(),name='post_edit'),
    path('create/',views.PostCreateView.as_view(),name='post_create'),
    path('delete/<int:pk>/',views.PostDeleteView.as_view(),name='post_delete'),
    path('follow/<int:pk>/',views.FollowingView.as_view(),name='user_follow'),
    path('unfollow/<int:pk>/',views.UnFollowingView.as_view(),name='user_unfollow'),
    path('comment-delete/<int:post_pk>/comment/<int:comment_pk>',views.DeleteCommentView.as_view(),name='delete_comment'),
]
