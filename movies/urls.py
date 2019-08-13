from django.urls import path
from . import views
from schedules import views as schedule_views


urlpatterns = [
    path('fetch/now_showing', views.fetch_now_showing),
    path('fetch/coming_soon', views.fetch_coming_soon),
    path('fetch/schedules', schedule_views.fetch_schedules),
    path('movies', views.retrieve_movies),
    path('movies/<uuid:movie_id>/schedules', views.retrieve_movie_schedules)
]