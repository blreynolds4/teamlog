from django.conf.urls import url

from . import views

app_name = 'team'

urlpatterns = [
    url(r'^(?P<team_name>[\w_\.\-\+@ ]+)$', views.TeamView.as_view(), name='team_detail'),
]
