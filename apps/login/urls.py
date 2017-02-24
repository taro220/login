from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^registration$', views.registration),
    url(r'^home$', views.home),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^addTravel$', views.addTravel),
    url(r'^processAddTravel$', views.processAddTravel),
    url(r'^destination/(?P<id>\d+)$', views.destination),
    url(r'^errorPage$', views.errorPage),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^', views.errorPage)
]
