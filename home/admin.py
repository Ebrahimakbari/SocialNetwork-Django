from django.contrib import admin
from .models import Post, Comment, PostLike
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','created_at','updated_at']
    prepopulated_fields = {'slug':('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'is_reply']


@admin.register(PostLike)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'is_liked','created_at']
    raw_id_fields = ['user', 'post']
