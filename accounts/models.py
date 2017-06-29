from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tagging.registry import register
from tagging.models import Tag


def _default_season_start():
    '''
    Set the default season start to what's in the settings.
    '''
    return settings.DEFAULT_SEASON_START


# Models for users and relations to tags
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    season_start = models.DateField(default=_default_season_start)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class UserTeam(models.Model):
    team = models.OneToOneField(Tag)
    owner = models.OneToOneField(UserProfile)
    is_closed = models.BooleanField(default=False)


# register the class for tagging
register(UserProfile)
