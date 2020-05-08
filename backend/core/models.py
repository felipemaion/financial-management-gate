from django.db import models

# Create your models here.
class DateTimeModel(models.Model):
    created_at = models.DateTimeField('created at', auto_now_add=True, blank=True)

    class Meta:
        abstract = True 

