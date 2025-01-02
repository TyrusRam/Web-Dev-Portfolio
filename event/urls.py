from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.user_logout, name="logout"),
    path('register', views.register, name='register'),
    path('create', views.create, name='create'),
    path('discover', views.discover, name="discover"),
    path('event/<event_id>/', views.event, name='event'),
    path('event', views.event, name='event'),
    path('rsvp/', views.rsvp, name='rsvp'),
    path('calendar', views.calendar, name='calendar'),
]