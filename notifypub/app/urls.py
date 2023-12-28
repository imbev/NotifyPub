from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('manage_notifications/', views.manage_notifications, name="manage_notifications"),
    path('manage_tokens/', views.manage_tokens, name="manage_tokens"),
]