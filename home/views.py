from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from tagging.utils import edit_string_for_tags
from posts.models import TeamPost


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        tags = edit_string_for_tags(request.user.userprofile.tags)
        print("User", request.user.username, "User tags", tags)
        posts = TeamPost.tagged.with_any(tags)

        return render(request, self.template_name, dict(posts=posts))
