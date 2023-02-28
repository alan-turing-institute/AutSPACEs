from django.urls import path, re_path
from server.apps.main import views

app_name = "main"

urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^signup/?$", views.signup, name="signup"),
    re_path(r"^signup1/?$", views.signup_frame4_test, name="signup_frame4_test"),
    re_path(r"^logout/?$", views.logout_user, name="logout"),
    re_path(r"^overview/?$", views.overview, name="overview"),
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
    path("delete/<uuid>/<title>/", views.delete_experience, name="delete_exp"),
    path("share_exp/", views.share_experience, name="share_exp"),
    path("edit/<uuid>/", views.share_experience, name="edit_exp"),
    path("moderate/<uuid>/", views.moderate_experience, name="moderate_exp"),
    path("view/<uuid>/", views.view_experience, name="view_exp"),
    path(
        "review_experience/<experience_id>/",
        views.review_experience,
        name="review_experience",
    ),
    path("my_stories/", views.my_stories, name="my_stories"),
    path("confirm_page/", views.confirmation_page, name="confirm_page"),
    path("about_us/", views.about_us, name="about_us"),
    path("what_autism_is/", views.what_autism_is, name="what_autism_is"),
    path("navigation/", views.navigation, name="navigation"),
    path("footer/", views.footer, name="footer"),
    path("registration/", views.registration, name="registration"),
]
