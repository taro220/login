from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^registration$', views.registration),
    url(r'^home$', views.home),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'errorPage$', views.errorPage),
    url(r'^', views.errorPage)
]
