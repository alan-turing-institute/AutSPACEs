from django.urls import path, re_path
from server.apps.main import views

app_name = "main"

urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^signup/?$", views.signup, name="signup"),
    re_path(r"^login/?$", views.login_user, name="login"),
    re_path(r"^logout/?$", views.logout_user, name="logout"),
    re_path(
        r"^public_experiences/?$",
        views.list_public_experiences,
        name="public_experiences",
    ),
    re_path(
        r"^moderate_public_experiences/?$",
        views.moderate_public_experiences,
        name="moderate_public_experiences",
    ),
    re_path(r"moderation_list/?$", views.moderation_list, name="moderation_list"),
    path("delete/<uuid>/", views.delete_experience, name="delete_exp"),
    path("share_exp/", views.share_experience, name="share_exp"),
    path("edit/<uuid>/", views.share_experience, name="edit_exp"),
    path("moderate/<uuid>/", views.moderate_experience, name="moderate_exp"),
    path("view/<uuid>/", views.view_experience, name="view_exp"),
    path("my_stories/", views.my_stories, name="my_stories"),
    path("about_us/", views.about_us, name="about_us"),
    path("what_autism_is/", views.what_autism_is, name="what_autism_is"),
    path("help/", views.help, name="help"),
    path("content_moderation_guidelines/", views.content_moderation_guidelines, name="content_moderation_guidelines"),
    path("participant_information/", views.participant_information, name="participant_information"),
    path("registration/", views.registration, name="registration"),
    path("single_story/<uuid>/",views.single_story,name="single_story"),
    path("success_confirm/", views.success_confirm, name="success_confirm"),
]
