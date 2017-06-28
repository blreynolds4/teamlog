from django.db import models
from django.contrib.auth.models import User
from tagging.registry import register
from datetime import timedelta


class TeamPost(models.Model):
    author = models.ForeignKey(User)
    message = models.TextField()
    post_date = models.DateField()
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-post_date', '-last_updated_at']

    def is_run(self):
        try:
            self.runpost
            return True
        except RunPost.DoesNotExist:
            return False


class RunPost(TeamPost):
    distance = models.FloatField()
    duration = models.IntegerField()
    route = models.CharField(max_length=64)
    details = models.TextField(default="")

    def display_time(self):
        td = timedelta(seconds=self.duration)
        return self._remove_leading_zeros(str(td))

    def pace(self):
        # drop the fractional seconds for pace
        pace = self.duration // self.distance
        td = timedelta(seconds=pace)

        return self._remove_leading_zeros(str(td))

    def _remove_leading_zeros(self, time_str):
        parts = time_str.split(':')
        skip = True
        new_parts = []
        for p in parts:
            if skip and p in ['0', '00']:
                pass
            else:
                skip = False
                new_parts.append(p)

        return ':'.join(new_parts)


# register run posts so they can be tagged
register(TeamPost)
