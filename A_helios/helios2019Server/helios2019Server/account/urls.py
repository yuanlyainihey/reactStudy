from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.UserRegisterList.as_view()),
    url(r'^user/$', views.UserLoginList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserLoginDetail.as_view()),
]
