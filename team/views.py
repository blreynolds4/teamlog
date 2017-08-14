from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Sum

from accounts.models import UserProfile
from posts.models import RunPost

from tagging.models import Tag
from tagging.utils import edit_string_for_tags


class TeamView(LoginRequiredMixin, TemplateView):
    template_name = 'team/team.html'

    def get(self, request, team_name):
        print("RENDERING Team Summary for", team_name)

        # Get all the runs for the team, group by user to show a total
        # for each user for the season order by most miles to least

        # May have to get all team posts an reduce to just runs to query by
        # tag
        t = Tag.objects.get(name=team_name)
        tags = edit_string_for_tags([t])
        team_members = UserProfile.tagged.with_any(tags)
        season_totals = []
        for athlete in team_members:
            user_runs = RunPost.objects.filter(author=athlete, post_date__gte=athlete.season_start).aggregate(season_total=Sum('distance'))
            season_totals.append(dict(user=athlete, season_total=user_runs['season_total']))

        sorted_totals = sorted(season_totals, key=lambda st: st['season_total'], reverse=True)

        return render(request,
                      self.template_name,
                      dict(user_totals=sorted_totals))
