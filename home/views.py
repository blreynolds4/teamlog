from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from tagging.utils import edit_string_for_tags
from posts.models import TeamPost
from datetime import date
from django.http import HttpResponse
from django.conf import settings


DATE_FORMAT = "%m-%d-%Y"


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        tags = edit_string_for_tags(request.user.userprofile.tags)
        posts = TeamPost.tagged.with_any(tags)

        today = date.today().strftime(DATE_FORMAT)
        return render(request, self.template_name, dict(posts=posts, today=today))


def version_view(request):
    return HttpResponse(settings.APP_VERSION, content_type="plain/text")
