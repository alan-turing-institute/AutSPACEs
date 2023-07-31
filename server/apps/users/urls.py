from django.urls import path, re_path
from server.apps.users import views

app_name = "servers.apps.users"

urlpatterns = [
    path("profile/", views.user_profile, name="profile"),
    path("greetings/", views.user_profile, {"first_visit": True}, name="greetings"),
    path("delete/", views.user_profile_delete, name="delete"),
]
