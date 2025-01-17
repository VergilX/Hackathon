from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path("", views.login, name='login'),
    path("register", views.register, name='register'),
    path("logout", views.logout, name='logout'),
    path("user", views.user, name="user"),
    path("edit", views.edit, name="edit"),
    path("edituser", views.edituser, name="edituser"),
    path("editalarms", views.editalarms, name="editalarms"),
]