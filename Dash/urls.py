from django.urls import path,re_path
from Dash import views, admin

urlpatterns = [
    path("", views.index, name='index'),
    path("index/", views.index, name='index'),
    path("login/", views.login, name='login'),
    path("logup/", views.logup, name='logup'),
    path("admin/", views.admin, name='admin'),
    path("logout/", views.logout, name='logout'),
    re_path(r"^admin/userinfo/(?P<url_code>[a-z/]+)?$", views.userinfo, name="userinfo"),
    re_path(r"^admin/log/(?P<url_code>[a-z/]+)?$", views.log, name="log"),
]