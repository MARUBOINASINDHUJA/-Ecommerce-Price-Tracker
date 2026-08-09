from django.contrib import admin
from django.urls import path
from tracker import views


urlpatterns = [
    path("", views.login_view, name="home"),
    path("admin/", admin.site.urls),
    path("test/", views.test, name="test"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("start-tracking/", views.start_tracking, name="start_tracking"),
]