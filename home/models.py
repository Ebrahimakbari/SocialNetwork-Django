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
    
    def get_absolute_url(self):
        return reverse("home:post_edit", kwargs={"pk": self.pk,"post_slug":self.slug})