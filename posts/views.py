from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from tagging.models import Tag
from tagging.utils import edit_string_for_tags

from .parsing import parse_duration
from .models import TeamPost, RunPost


class RunView(LoginRequiredMixin, TemplateView):
    template_name = "posts/edit_run.html"

    def get(self, request):
        return render(request, 'posts/edit_run.html')

    def post(self, request):
        if request.POST['run_distance'] and request.POST['run_time']:
            run = RunPost(author=request.user,
                          duration=parse_duration(request.POST['run_time']),
                          distance=float(request.POST['run_distance']),
                          message=request.POST['run_description'],
                          post_date=request.POST['run_date'])
            run.save()
            print("User", request.user.username, "Tags", edit_string_for_tags(request.user.userprofile.tags))
            Tag.objects.update_tags(run.teampost_ptr, edit_string_for_tags(request.user.userprofile.tags))

            return redirect("home")
        else:
            return render(request,
                          self.template_name,
                          dict(error="ERROR:  Run requires at least time and distance."))


class MessageView(LoginRequiredMixin, TemplateView):
    template_name = "posts/edit_msg.html"

    def get(self, request):
        return render(request, 'posts/edit_msg.html')

    def post(self, request):
        if request.POST['message']:
            msg = TeamPost(author=request.user,
                           message=request.POST['message'],
                           post_date=request.POST['msg_date'])
            msg.save()
            print("User", request.user.username, "Tags", edit_string_for_tags(request.user.userprofile.tags))
            Tag.objects.update_tags(msg, edit_string_for_tags(request.user.userprofile.tags))

            return redirect("home")
        else:
            return render(request,
                          self.template_name,
                          dict(error="ERROR:  Message is required."))
