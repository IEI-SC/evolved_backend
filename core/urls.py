from django.urls import path
from . import views
from django.shortcuts import render
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'team-members', views.TeamMemberViewSet)


urlpatterns = [
    path('', views.home, name='home'),
    
    # Events
    path('events/', views.event_list, name='events'),
    # core/urls.py
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    
    # Team
    path('team/', views.team_view, name='team'),
    
    # Contact
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    
    # About (Static Page)
    path('about/', views.about, name='about'),

    # API endpoints
    path('api/team/', views.api_team_members, name='api_team'),
    path('api/team/structured/', views.api_team_structured, name='api_team_structured'),


    # API endpoints
    path('api/', include(router.urls)),
    path('api/team/clear/', views.team_data_api, name='team_api'),

    # In core/urls.py, add this path
    path('api/events/', views.api_events, name='api_events'),

]