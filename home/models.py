from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse
from .managers import PostManager

User = get_user_model()




class Post(models.Model):
    PUBLISHED = 'PUB'
    PRIVATE = 'PRI'
    
    publish_status = [
        (PUBLISHED,'published'),
        (PRIVATE,'private'),
    ]
    
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/')
    slug = models.SlugField(blank=True, null=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=publish_status,default=PUBLISHED)
    
    objects = models.Manager() 
    published = PostManager()

    class Meta:
        verbose_name = ("Post")
        verbose_name_plural = ("Posts")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    def save(self):
        self.slug = slugify(self.title)
        return super().save()
    
    def get_likes_count(self):
        return self.likes.filter(is_liked=True).count()
    
    def get_absolute_url(self):
        return reverse("home:post_edit", kwargs={"pk": self.pk,"post_slug":self.slug})
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    reply = models.ForeignKey("self", related_name="replys", on_delete=models.CASCADE, null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Comment")
        verbose_name_plural = ("Comments")

    def __str__(self):
        return f'{self.user} on post {self.post}'


class PostLike(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)    

    class Meta:
        verbose_name = ("PostLike")
        verbose_name_plural = ("PostLikes")

    def __str__(self):
        return f'user {self.user} liked post {self.post}'