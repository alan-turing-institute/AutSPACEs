from django.urls import path, re_path
from server.apps.main import views

app_name = 'main'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^signup/?$', views.signup, name='signup'),
    re_path(r'^signup1/?$', views.signup_frame4_test, name='signup_frame4_test'),
    re_path(r'^logout/?$', views.logout_user, name='logout'),
    re_path(r'^overview/?$', views.overview, name='overview'),
    re_path(r'^view_experiences/?$', views.list_public_experiences,
        name='view_experiences'),
    re_path(r'^moderate_public_experiences/?$', views.moderate_public_experiences,
        name='moderate_public_experiences'),
    re_path(r'^list/?$', views.list_files, name='list'),
    
    path('delete/<uuid>/<title>/', views.delete_experience, name='delete_exp'),
    path('share_exp/', views.share_experience, name='share_exp'),
    path('edit/<uuid>/', views.share_experience, name='edit_exp'),
    
    path('review_experience/<experience_id>/',
         views.review_experience,
         name='review_experience'),
    path('make_non_viewable/<oh_file_id>/<file_uuid>/',
         views.make_non_viewable,
         name='make_non_viewable'),
    path('make_viewable/<oh_file_id>/<file_uuid>/',
         views.make_viewable,
         name='make_viewable'),
    path('make_non_research/<oh_file_id>/<file_uuid>/',
         views.make_non_research,
         name='make_non_research'),
    path('make_research/<oh_file_id>/<file_uuid>/',
         views.make_research,
         name='make_research'),
    path('my_stories/', views.my_stories, name="my_stories"),
    path('confirm_page/', views.confirmation_page, name="confirm_page"),
    path('about_us/', views.about_us, name="about_us"),
    path('what_autism_is/', views.what_autism_is, name="what_autism_is"),
    path('navigation/', views.navigation, name="navigation"),
    path('footer/', views.footer, name="footer"),
    path('registration/', views.registration, name="registration"),

]
