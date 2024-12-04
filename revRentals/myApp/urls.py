from django.urls import path
from .views import *
from .garage_views import *
from .admin_views import *
from .reservations_views import *
from .vehicle_views import GetVIN
from myApp.vehicle_views import *
from myApp.gear_views import *

import logging

logger = logging.getLogger(__name__)


urlpatterns = [
    # User URLs
    # Profile Login/Register/Details
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/profile-details/', ProfileDetailsView.as_view(), name='profile-details'),
    path('api/get-profile-id/<str:username>/', GetProfileIDView.as_view(), name='get-profile-id'),
    
    # Marketplace
    path('api/motorized-vehicles/', ViewAllMotorizedVehicles.as_view(), name='view-all-motorized-vehicles'),
    path('api/motorized-vehicles/<str:vin>/',ViewMaintenanceRecords.as_view(), name = 'view-maintenance-records'),
        
    path('api/storage-lots/', ViewAllStorageLots.as_view(), name='view-all-storage-lots'),
    path('api/gear-items/', ViewAllGearItems.as_view(), name='view-all-gear-items'),
    
    # Reservations for items
    path('api/add-reservation/', AddReservationView.as_view(), name='add-reservation'),
    
    # Agreements
    path('api/add-agreement/', AddAgreementView.as_view(), name='add-agreement'),     
    
    # Transactions
    path('api/add-transaction/', AddTransactionView.as_view(), name='add-transaction'),  
    
    # Garage
    path('api/get-garage-id/<int:profile_id>/', GetGarageIDView.as_view(), name='get_garage_id'),
    path('api/add-listing/', AddMotorizedVehicleView.as_view(), name='add-listing'),
    path('api/add-gear-listing/', AddGearView.as_view(), name = 'add-gear'),
    path('api/view-listing/', ViewAllGarageItemsView.as_view(), name='view-listing'),
    path('api/add-maintenance-records/', AddMaintenanceRecordsView.as_view(), name='add-maintenance-records'),
    
    # Admin URLs
    path('api/admin-login/', AdminLoginView.as_view(), name='admin-login'),
    path('api/get-admin-id/', GetAdminIDView.as_view(), name='get-admin-id'),
    # Agreements, Reservations, Transactions
    path('api/agreements/', ViewAllAgreements.as_view(), name ='view-agreements'),
    path('api/reservations/', ViewAllReservations.as_view(), name ='view-reservations'),
    path('api/view-transaction/<int:reservation_no>/', GetTransactionView.as_view(), name = 'view-transaction' ),
    path('api/view-agreement/<int:reservation_no>/', GetAgreementView.as_view(), name = 'view-agreement' ),
    
    # Lots
    path('api/add-lot-listing/',AddLotListing.as_view(), name = 'add-lot-listing'),
    path('api/edit-lot-listing/',EditLotListing.as_view(), name = 'edit-lot-listing'),

    # Marketplace
    #path('filter-by-color-view/',SearchByColorView.as_view(), name='filter_by_color_view'),
    path('filter-by-color/', search_by_color_view, name='filter_by_color'),
    path('filter-by-price/', search_by_rental_price_view, name='filter_by_price'),
    path('filter-by-mileage/', search_by_mileage_view, name='filter_by_mileage'),
    path('filter-by-insurance/', search_by_insurance_view, name='filter_by_insurance'),
    path('filter-by-vehicle/', search_by_vehicle_view, name='filter_by_insurance'),

    #Gear
    path('filter-by-gear/', search_gear_by_type_view, name='filter-by-gear'),
    path('filter-by-gear-price/', search_gear_by_rental_price_view, name='filter-by-gear-price'),
    path('filter-by-size/', search_gear_by_size_view, name='filter-by-size'),
    path('filter-by-material/', search_gear_by_material_view, name='filter-by-material'),
    path('filter-by-brand/', search_gear_by_brand_view, name='filter-by-brand'),
]
