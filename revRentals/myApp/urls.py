from django.urls import path
from .views import LoginView, RegisterView, GetGarageIDView
from .garage_views import AddMotorizedVehicleView, ViewAllGarageItemsView, ViewAllMotorizedVehicles, ViewAllStorageLots, ViewAllGearItems
from .admin_views import AdminLoginView

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/get-garage-id/<int:profile_id>/', GetGarageIDView.as_view(), name='get_garage_id'),
    path('api/add-listing/', AddMotorizedVehicleView.as_view(), name='add-listing'),
    path('api/view-listing/', ViewAllGarageItemsView.as_view(), name='view-listing'),
    path('api/motorized-vehicles/', ViewAllMotorizedVehicles.as_view(), name='view-all-motorized-vehicles'),
    path('api/storage-lots/', ViewAllStorageLots.as_view(), name='view-all-storage-lots'),
    path('api/gear-items/', ViewAllGearItems.as_view(), name='view-all-gear-items'),

    # Admin URLs
    path('api/admin-login/',AdminLoginView.as_view(), name='admin-login')
]
