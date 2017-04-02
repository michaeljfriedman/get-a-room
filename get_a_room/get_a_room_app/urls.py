from django.conf.urls import url
from . import views

app_name = 'get_a_room_app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
