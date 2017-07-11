from django.conf.urls import url

from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^msg$', views.MessageView.as_view(), name='new_msg'),
    url(r'^msg/(?P<msg_id>[0-9]+)$', views.MessageView.as_view(), name='edit_msg'),
    url(r'^run$', views.RunView.as_view(), name='new_run'),
    url(r'^run/(?P<post_id>[0-9]+)$', views.RunView.as_view(), name='edit_run'),
    # deletes all post types
    url(r'^(?P<post_id>[0-9]+)$', views.DeleteView.as_view(), name='delete'),
]
