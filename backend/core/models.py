from django.db import models

# Create your models here.
class BaseTimeModel(models.Model):
    created_at = models.DateTimeField('created at', auto_now_add=True, blank=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        abstract = True 
