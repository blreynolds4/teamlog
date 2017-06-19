from django.conf.urls import url

from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^msg$', views.MessageView.as_view(), name='edit_msg'),
    url(r'^run$', views.RunView.as_view(), name='edit_run'),
]
