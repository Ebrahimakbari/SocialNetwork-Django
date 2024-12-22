from django.contrib import admin
from .models import Post, Comment
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','created_at','updated_at']
    prepopulated_fields = {'slug':('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'is_reply']
    raw_id_fields = ['user', 'post', 'reply']
