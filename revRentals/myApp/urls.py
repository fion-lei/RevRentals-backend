from django.urls import path
from .views import add_profile_view, check_profile_view

urlpatterns = [
    path('api/profile/add/', add_profile_view, name='add_profile'),
    path('api/profile/check/', check_profile_view, name='check_profile'),
]