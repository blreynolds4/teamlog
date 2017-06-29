from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from tagging.utils import edit_string_for_tags
from posts.models import TeamPost, RunPost
from accounts.models import UserProfile
from django.db.models import Sum
from datetime import date, timedelta
from django.http import HttpResponse
from django.conf import settings


DATE_FORMAT = "%m-%d-%Y"


def get_start_of_week(d):
    '''
    Get the first day of the week for the given date.
    '''
    delta = timedelta(days=(d.weekday()+1))
    return d - delta


def get_query_date_range(start, end):
    '''
    Get a date range for the query
    '''
    DATE_QUERY_STRING = "%Y-%m-%d"
    return [start.strftime(DATE_QUERY_STRING), end.strftime(DATE_QUERY_STRING)]


def total_or_zero(t):
    return t if t is not None else 0


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        now = date.today()

        tags = edit_string_for_tags(request.user.userprofile.tags)
        posts = TeamPost.tagged.with_any(tags)

        run_stats = dict()

        # get the total miles
        temp = RunPost.objects.filter(author=request.user.userprofile).aggregate(total=Sum('distance'))
        run_stats['total'] = total_or_zero(temp['total'])

        # total for the season
        season_start = request.user.userprofile.season_start
        temp = RunPost.objects.filter(author=request.user.userprofile,
                                      post_date__gte=season_start).aggregate(total=Sum('distance'))
        run_stats['season'] = total_or_zero(temp['total'])

        # total for the week
        week_start = get_start_of_week(now)
        temp = RunPost.objects.filter(author=request.user.userprofile,
                                      post_date__range=get_query_date_range(week_start, now)).aggregate(total=Sum('distance'))
        run_stats['week'] = total_or_zero(temp['total'])

        # get the teams so they can be shown
        teams = request.user.userprofile.tags

        today = now.strftime(DATE_FORMAT)
        return render(request,
                      self.template_name,
                      dict(posts=posts, today=today, teams=teams, run_stats=run_stats))


def version_view(request):
    return HttpResponse(settings.APP_VERSION, content_type="plain/text")
