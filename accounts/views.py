from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile


class SignupView(TemplateView):
    template_name = "accounts/signup.html"

    def post(self, request):
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username']).select_related('userprofile')
                return render(request, self.template_name, dict(error="Sign up failed:  Username already in use."))
            except User.DoesNotExist:
                if request.POST['teams'] not in ['', None]:
                    user = User.objects.create_user(username=request.POST['username'],
                                                    password=request.POST['password1'])
                    user.userprofile.tags = request.POST['teams']
                    user.save()
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, self.template_name, dict(error="Sign up failed:  Team name is required."))

        else:
            return render(request, self.template_name, dict(error="Sign up failed:  Passwords do not match."))


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


class LogoutView(TemplateView):
    def post(self, request):
        logout(request)
        return redirect('home')
