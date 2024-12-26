from django.db import models
from django.db.models import Q



class PostManager(models.Manager):
    def get_queryset(self,*args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(status='PUB')
    
    def search(self,q, *args, **kwargs):
        return self.get_queryset(*args, **kwargs).filter(
            Q(title__icontains=q) | Q(content__icontains=q)
            )
