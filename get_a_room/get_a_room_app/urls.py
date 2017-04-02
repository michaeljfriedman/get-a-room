from django.conf.urls import url
from . import views

app_name = 'get_a_room_app'
urlpatterns = [
    url(r'^slide-panel/(?P<building>[a-z\-]+)/$', views.slide_panel, name='slide-panel'),
    url(r'^slide-panel-test/', views.slide_panel_test, name='slide-panel-test'),
    url(r'^$', views.index, name='index'),
]
