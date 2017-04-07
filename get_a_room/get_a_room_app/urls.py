from django.conf.urls import url
from . import views

app_name = 'get_a_room_app'
urlpatterns = [
    url(r'^test/', views.test, name='test'),
    url(r'^stats/building/(?P<building>[0-9a-z\-]+)/$', views.stats_building, name='stats_building'),
    url(r'^stats/most-recent/$', views.stats_most_recent, name='stats_most_recent'),
    url(r'^slide-panel-test/', views.slide_panel_test, name='slide-panel-test'),
    url(r'^$', views.index, name='index'),
]
