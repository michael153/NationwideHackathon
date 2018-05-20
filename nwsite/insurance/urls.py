from django.conf.urls import url

from . import views

app_name = 'insurance'
urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^map/$', views.map_view, name='map'),
    url(r'^drivinginfo/$', views.drivinginfo_view, name='drivinginfo'),
]