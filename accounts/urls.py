from django.conf.urls import url

from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^signup/', views.SignupView.as_view(), name='signup'),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logogout/', views.LogoutView.as_view(), name='logout'),
]
