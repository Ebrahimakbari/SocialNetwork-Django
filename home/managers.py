from django.db import models


class PostManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        qs = super().get_queryset()
        return qs.filter(status='PUB')
