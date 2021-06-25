from django.conf.urls import url
from django.urls import path

from server.apps.main import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/?$', views.logout_user, name='logout'),
    url(r'^overview/?$', views.overview, name='overview'),
    url(r'^public_experiences/?$', views.list_public_experiences,
        name='public_experiences'),
    url(r'^moderate_public_experiences/?$', views.moderate_public_experiences,
        name='moderate_public_experiences'),
    url(r'^upload/?$', views.upload, name='upload'),
    url(r'^list/?$', views.list_files, name='list'),
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
    path('my_stories/', views.my_stories, name="my-stories"),
]
