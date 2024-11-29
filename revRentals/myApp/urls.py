from django.urls import path
from .views import *
from .garage_views import *
from .admin_views import *
from .reservations_views import *

urlpatterns = [
    # User URLs
    # Profile Login/Register/Details
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/profile-details/', ProfileDetailsView.as_view(), name='profile-details'),
    path('api/get-profile-id/<str:username>/', GetProfileIDView.as_view(), name='get-profile-id'),
    
    # Marketplace
    path('api/motorized-vehicles/', ViewAllMotorizedVehicles.as_view(), name='view-all-motorized-vehicles'),
    path('api/storage-lots/', ViewAllStorageLots.as_view(), name='view-all-storage-lots'),
    path('api/gear-items/', ViewAllGearItems.as_view(), name='view-all-gear-items'),
    
    # Reservations for items
    path('api/motorcycle-reservation/', AddMotorcycleReservationView.as_view(), name='add-motorcycle-reservation'),
    path('api/gear-reservation/', AddGearReservationView.as_view(), name='add-gear-reservation'), 
    path('api/lot-reservation/', AddLotReservationView.as_view(), name='add-lot-reservation'), 
    
    # Agreements
    
    # Transactions
    
    # Garage
    path('api/get-garage-id/<int:profile_id>/', GetGarageIDView.as_view(), name='get_garage_id'),
    path('api/add-listing/', AddMotorizedVehicleView.as_view(), name='add-listing'),
    # TODO: Add gear
    path('api/add-gear-listing/', AddGearView.as_view(), name = 'add-gear'),
    path('api/view-listing/', ViewAllGarageItemsView.as_view(), name='view-listing'),


    # Admin URLs
    path('api/admin-login/',AdminLoginView.as_view(), name='admin-login'),
    # Agreements, Reservations, Transactions
    path('api/agreements/', ViewAllAgreements.as_view(), name ='view-agreements'),
    path('api/reservations/', ViewAllReservations.as_view(), name ='view-reservations'),
    # Lots
    path('api/add-lot-listing/',AddLotListing.as_view(), name = 'add-lot-listing'),
    path('api/edit-lot-listing/',EditLotListing.as_view(), name = 'edit-lot-listing'),

]
