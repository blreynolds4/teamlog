from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from tagging.models import Tag
from tagging.utils import edit_string_for_tags
from datetime import datetime, date

from .parsing import parse_duration
from .models import TeamPost, RunPost

DATE_FORMAT = "%m-%d-%Y"


def parse_date(date_str):
    dt = datetime.strptime(date_str, DATE_FORMAT)
    return dt.date()


def save_submitted_run_data(values):
    result = dict()
    result['today'] = values.get('run_date', '')
    result['distance'] = values.get('run_distance', '')
    result['duration'] = values.get('run_duration', '')
    result['route'] = values.get('run_route', '')
    result['description'] = values.get('run_description', '')
    result['details'] = values.get('run_details', '')

    return result


def save_submitted_msg_data(values):
    result = dict()
    result['message'] = values.get('message', '')

    return result


class RunView(LoginRequiredMixin, TemplateView):
    template_name = "posts/edit_run.html"

    def get(self, request):
        return render(request, 'posts/edit_run.html', dict(today=date.today()))

    def post(self, request):
        run = save_submitted_run_data(request.POST)
        try:
            post_date = parse_date(request.POST['run_date'])

            if request.POST['run_distance'] and request.POST['run_time']:
                run = RunPost(author=request.user.userprofile,
                              duration=parse_duration(request.POST['run_time']),
                              distance=float(request.POST['run_distance']),
                              message=request.POST['run_description'],
                              route=request.POST['run_route'],
                              details=request.POST['run_details'],
                              post_date=post_date)
                run.save()
                print("User", request.user.username, "Tags", edit_string_for_tags(request.user.userprofile.tags))
                Tag.objects.update_tags(run.teampost_ptr, edit_string_for_tags(request.user.userprofile.tags))

                return redirect("home")
            else:
                return render(request,
                              self.template_name,
                              dict(error="Run requires at least time and distance.", run=run))
        except ValueError:
            return render(request,
                          self.template_name,
                          dict(error="Date format must be 01-01-2017 (leading zeroes required)", run=run))


class MessageView(LoginRequiredMixin, TemplateView):
    template_name = "posts/edit_msg.html"

    def get(self, request):
        return render(request, 'posts/edit_msg.html')

    def post(self, request):
        msg = save_submitted_msg_data(request.POST)
        try:
            post_date = parse_date(request.POST['msg_date'])
            if request.POST['message']:
                msg = TeamPost(author=request.user.userprofile,
                               message=request.POST['message'],
                               post_date=post_date)
                msg.save()
                print("User", request.user.username, "Tags", edit_string_for_tags(request.user.userprofile.tags))
                Tag.objects.update_tags(msg, edit_string_for_tags(request.user.userprofile.tags))

                return redirect("home")
            else:
                return render(request,
                              self.template_name,
                              dict(error="Message is required.", msg=msg))
        except ValueError:
            return render(request,
                          self.template_name,
                          dict(error="Date format must be 01-01-2017 (leading zeroes required)",
                               msg=msg))
