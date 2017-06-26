from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^add_secret/(?P<user_id>\d+)/(?P<current_page>\w+)$', views.add_secret, name = "add_secret"),
    url(r'^add_like/(?P<user_id>\d+)/(?P<secret_id>\d+)/(?P<current_page>\w+)$', views.add_like, name = "add_like"),
    url(r'^remove/(?P<secret_id>\d+)$', views.remove, name = "remove"),
    url(r'^popular$', views.popular, name = "popular"),
]