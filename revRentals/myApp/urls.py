from django.urls import path
from .views import LoginView, RegisterView
from .profile_views import add_profile_view

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegisterView.as_view(), name='register'),
]
