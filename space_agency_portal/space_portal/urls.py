from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('missions/', views.missions, name='missions'),
    path('missions/<slug:slug>/', views.mission_detail, name='mission_detail'),
    path('astronauts/', views.astronauts, name='astronauts'),
    path('astronauts/<int:pk>/', views.astronaut_detail, name='astronaut_detail'),
    path('launches/', views.launches, name='launches'),
    path('news/', views.news, name='news'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('api/mission-stats/', views.api_mission_stats, name='api_mission_stats'),
]
