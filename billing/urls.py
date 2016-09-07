from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^card/$', views.CardCreateEdit.as_view(), name='card_create'),
    url(r'^card/delete/$', views.CardDelete.as_view(), name='card_delete'),
)