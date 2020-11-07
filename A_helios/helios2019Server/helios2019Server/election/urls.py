from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^administrators/$', views.EletionAminitratorListCreate.as_view()),
    url(r'^administrators/(?P<pk>[0-9]+)$',
        views.EletionAminitratorUpdateDestroy.as_view()),
    url(r'^elections/$', views.EletionListCreate.as_view()),
    url(r'^elections/(?P<pk>[0-9]+)$',
        views.EletionRetrieveUpdateDestroy.as_view()),
    url(r'^elections/(?P<pk>[0-9]+)/bbs$',
        views.BbsRetrieve.as_view()),
    url(r'^voters/$', views.VoterList.as_view()),
    url(r'^voters/(?P<pk>[0-9]+)$',
        views.VoterRetrieveUpdateDestroy.as_view()),
    url(r'^verifyvoters/$', views.VerifyVoterList.as_view()),
]
