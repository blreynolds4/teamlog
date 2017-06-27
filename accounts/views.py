from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserTeam
from tagging.models import Tag
from django.conf import settings
from django.urls import reverse


def queryable_tag(raw_name):
    '''
    This normalizes the input to lower case if needed
    so we can query to see if the tag exists already
    '''
    result = raw_name
    if settings.FORCE_LOWERCASE_TAGS:
        result = raw_name.lower()

    return result


def clean_team_name(raw_name):
    '''
    Add enclosing quotes if the raw name includes spaces.
    This prevents it from creating multiple tags when we just want one.
    '''
    if ' ' in raw_name:
        return '"'+raw_name+'"'
    else:
        return raw_name


def join_url(team_tag):
    '''
    Generate a url by name to the join page for this new team.
    '''
    return "{0}?team={1}".format(reverse('accounts:join'), team_tag.id)


class SignupView(TemplateView):
    template_name = "accounts/signup.html"
    welcome_template = "accounts/welcome.html"

    def post(self, request):
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, self.template_name, dict(error="Sign up failed:  Username already in use."))
            except User.DoesNotExist:
                if request.POST['team'] not in ['', None]:
                    # make sure the team doesn't already exist
                    try:
                        team = queryable_tag(request.POST['team'])
                        Tag._default_manager.get(name=team)
                        return render(request, self.template_name, dict(error="Sign up failed:  Team name already in use."))
                    except Tag.DoesNotExist:
                        user = User.objects.create_user(username=request.POST['username'],
                                                        password=request.POST['password1'])
                        team = clean_team_name(team)
                        user.userprofile.tags = team
                        user.save()
                        team_tag = user.userprofile.tags[0]
                        userteam = UserTeam(team=team_tag, owner=user.userprofile)
                        userteam.save()

                        login(request, user)
                        return render(request,
                                      self.welcome_template,
                                      dict(share_url=request.build_absolute_uri(join_url(team_tag))))
                else:
                    return render(request, self.template_name, dict(error="Sign up failed:  Team name is required."))

        else:
            return render(request, self.template_name, dict(error="Sign up failed:  Passwords do not match."))


class JoinView(TemplateView):
    template_name = "accounts/join.html"

    def get(self, request):
        # there has to be a team query parameter for the user to join
        # if it is missing it's an error.
        # the parameter should be a tag id rather than a team name.
        team_id = request.GET.get('team', '')
        if team_id == '':
            return render(request, self.template_name, dict(error="Team to join is missing from url.  Contact your coach to ensure you have the correct url."))
        else:
            # lookup the tag for the team to join
            try:
                Tag._default_manager.get(pk=team_id)
                # embed the team id so it is sent along with the signup
                return render(request, self.template_name, dict(team=team_id))

            except Tag.DoesNotExist:
                return render(request, self.template_name, dict(error="Team to join does not exist.  Contact your coach to ensure you the correct url."))

    def post(self, request):
        team_id = request.POST.get('team', '')
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, self.template_name, dict(error="Sign up failed:  Username already in use.", team=team_id))
            except User.DoesNotExist:
                if team_id not in ['', None]:
                    # get the team
                    try:
                        team = Tag._default_manager.get(pk=team_id)
                        coach_team = UserTeam.objects.get(team=team)
                        if not coach_team.is_closed:
                            user = User.objects.create_user(username=request.POST['username'],
                                                            password=request.POST['password1'])
                            user.userprofile.tags = clean_team_name(team.name)
                            user.save()

                            login(request, user)
                            return redirect('home')
                        else:
                            return render(request, self.template_name, dict(error="Sign up failed:  Team to join is closed to new members. Please contact the coach.", team=team_id))
                    except Tag.DoesNotExist:
                        return render(request, self.template_name, dict(error="Sign up failed:  Team to join was not found. Get the correct url from your coach.", team=team_id))
                    except UserTeam.DoesNotExist:
                        return render(request, self.template_name, dict(error="Sign up failed:  Team to join was not found. Get the correct url from your coach.", team=team_id))
                else:
                    return render(request, self.template_name, dict(error="Sign up failed:  Team missing, get the correct url from your coach.", team=team_id))
        else:
            return render(request, self.template_name, dict(error="Sign up failed:  Passwords do not match.", team=team_id))


class LoginView(TemplateView):
    template_name = "accounts/login.html"

    def post(self, request):
        user = user = authenticate(request,
                                   username=request.POST['username'],
                                   password=request.POST['password'])
        if user is not None:
            login(request, user)
            if ('next' in request.POST) and (request.POST['next'] is not None):
                return redirect(request.POST['next'])
            return redirect('home')
        else:
            return render(request, self.template_name, dict(error="Invalid username or password."))


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get(self, request):
        owned_teams = UserTeam.objects.filter(owner=request.user.userprofile)
        for ot in owned_teams:
            ot.join_url = request.build_absolute_uri(join_url(ot.team))
            print("JOIN URL", ot.join_url)
        return render(request, self.template_name, dict(teams=owned_teams))

    def post(self, request):
        team = queryable_tag(request.POST['team'])
        tag = Tag._default_manager.get(name=team)
        user_team = UserTeam.objects.get(owner=request.user.userprofile, team=tag)
        user_team.is_closed = request.POST['is_closed'] == '1'
        user_team.save()

        owned_teams = UserTeam.objects.filter(owner=request.user.userprofile)
        return render(request, self.template_name, dict(teams=owned_teams))


class LogoutView(TemplateView):
    def post(self, request):
        logout(request)
        return redirect('home')
