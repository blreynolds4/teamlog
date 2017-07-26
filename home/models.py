from django.db import models
from accounts.models import UserProfile

# Create your models here.


class Feedback(models.Model):
    author = models.ForeignKey(UserProfile)
    message = models.TextField()
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_updated_at']
