from django.conf.urls import url

from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^signup/', views.SignupView.as_view(), name='signup'),
    url(r'^join/', views.JoinView.as_view(), name='join'),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^profile/', views.ProfileView.as_view(), name='profile'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
]
