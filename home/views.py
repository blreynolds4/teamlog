from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from tagging.utils import edit_string_for_tags
from posts.models import TeamPost, RunPost
from posts.parsing import parse_duration, remove_leading_zeros
from .models import Feedback
from django.db.models import Sum
from datetime import date, timedelta
from django.http import HttpResponse
from django.conf import settings

from math import floor


def get_query_date_range(start, end):
    '''
    Get a date range for the query
    '''
    DATE_QUERY_STRING = "%Y-%m-%d"
    return [start.strftime(DATE_QUERY_STRING), end.strftime(DATE_QUERY_STRING)]


def total_or_zero(t):
    return t if t is not None else 0


def _get_achievements(season_total):
    '''
    return a list of achievements for the user based
    on their season total.
    '''
    return [a for a in settings.ACHIEVEMENTS if a <= season_total]


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        now = date.today()
        print("RENDERING HOME for DATE", now)

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

        run_stats['achievements'] = _get_achievements(run_stats['season'])

        # total for the week
        week_start = _get_first_sunday(now)
        temp = RunPost.objects.filter(author=request.user.userprofile,
                                      post_date__range=get_query_date_range(week_start, now)).aggregate(total=Sum('distance'))
        run_stats['week'] = total_or_zero(temp['total'])

        # get the teams so they can be shown
        teams = request.user.userprofile.tags

        today = now.strftime(settings.DATE_FORMAT)
        return render(request,
                      self.template_name,
                      dict(user=request.user,
                           posts=posts,
                           today=today,
                           teams=teams,
                           run_stats=run_stats))


def _get_first_sunday(start_date):
    if start_date.weekday() == 6:
        return start_date
    else:
        # figure out sunday and return that
        delta = timedelta(days=(start_date.weekday()+1))
        return start_date - delta


def _update_run(calendar, run):
    week = None
    # get the right row in the calendar
    for w in calendar:
        if run.post_date >= w['week_of']:
            week = w
        else:
            break

    # update the run in it's week
    for d in week['runs']:
        if run.post_date == d['day']:
            d['distance'] = d['distance'] + run.runpost.distance


def build_calendar(start_date, runs):
    '''
    Build a list of weeks with a list of workouts for each week
    '''
    calendar = []
    if len(runs) > 0:
        day_delta = timedelta(days=1)
        week_delta = timedelta(days=7)
        week_start = _get_first_sunday(start_date)
        last_run = runs[-1].post_date
        calendar = []
        while last_run >= week_start:
            week = dict(week_of=week_start, runs=[])
            calendar.append(week)
            day = week_start
            week_start = week_start + week_delta

            # fill in the days before next week
            while day < week_start:
                week['runs'].append(dict(day=day, distance=0, total=0))
                day = day + day_delta

        for r in runs:
            _update_run(calendar, r)

        for w in calendar:
            dists = [r['distance'] for r in w['runs']]
            w['total'] = sum(dists)

    print("Calendar", calendar)
    return calendar


class UserHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/userhome.html'

    def get(self, request, username):
        print("User View", username)
        now = date.today()

        auth_user = User.objects.get(username=username)
        user = auth_user.userprofile

        tags = edit_string_for_tags(user.tags)
        # filter the posts to just this user
        posts = TeamPost.tagged.with_any(tags).filter(author=user).order_by("post_date")

        run_stats = dict()

        run_stats['calendar'] = build_calendar(user.season_start,
                                               [r for r in posts if r.is_run()])

        # now that calendar is build, re-sort the runs to most recent first
        #posts = TeamPost.tagged.with_any(tags).filter(author=user)
        posts = sorted(posts, key=lambda k: k.post_date, reverse=True)

        # get the total miles
        temp = RunPost.objects.filter(author=user).aggregate(total=Sum('distance'))
        run_stats['total'] = total_or_zero(temp['total'])

        # total for the season
        season_start = user.season_start
        temp = RunPost.objects.filter(author=user,
                                      post_date__gte=season_start).aggregate(total=Sum('distance'))
        run_stats['season'] = total_or_zero(temp['total'])

        run_stats['achievements'] = _get_achievements(run_stats['season'])

        # total for the week
        week_start = _get_first_sunday(now)
        print("Start of week", week_start)
        temp = RunPost.objects.filter(author=user,
                                      post_date__range=get_query_date_range(week_start, now)).aggregate(total=Sum('distance'))
        run_stats['week'] = total_or_zero(temp['total'])

        # get the teams so they can be shown
        teams = user.tags

        today = now.strftime(settings.DATE_FORMAT)
        return render(request,
                      self.template_name,
                      dict(user=auth_user,
                           posts=posts,
                           today=today,
                           teams=teams,
                           run_stats=run_stats))


def version_view(request):
    return HttpResponse(settings.APP_VERSION, content_type="plain/text")


class FeedbackView(LoginRequiredMixin, TemplateView):
    template_name = "home/feedback.html"

    def post(self, request):
        '''
        Create a feedback record.
        '''
        if request.POST['feedback']:
            m = Feedback(author=request.user.userprofile,
                         message=request.POST['feedback'])
            m.save()

            return redirect("home")
        else:
            return render(request,
                          self.template_name,
                          dict(error="Please provide your feedback"))


class ConvertView(TemplateView):
    template_name = 'home/convert.html'
    FIVE_K_DISTANCE = 3.1

    def post(self, request):
        '''
        do a conversion to 5k time.
        '''
        if request.POST['run_distance'] and request.POST['time']:

            duration = parse_duration(request.POST['time'])
            distance = float(request.POST['run_distance'])
            print("Converting", duration, "for", distance)
            five_k_time = timedelta(seconds=floor((duration / distance) * self.FIVE_K_DISTANCE))

            print("5k Time", five_k_time)
            return render(request,
                          self.template_name,
                          dict(conversion=remove_leading_zeros(str(five_k_time))))
        else:
            return render(request,
                          self.template_name,
                          dict(error="Please provide distance and time"))
