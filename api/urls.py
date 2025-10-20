"""
API URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


router = DefaultRouter()
router.register(r'profile', views.UserProfileViewSet, basename='profile')
router.register(r'internships', views.InternshipViewSet, basename='internship')
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'hackathons', views.HackathonViewSet, basename='hackathon')
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'resume', views.ResumeViewSet, basename='resume')

urlpatterns = [
   
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    

    path('webhook/achievement/', views.webhook_achievement, name='webhook-achievement'),
    
    path('', include(router.urls)),
]