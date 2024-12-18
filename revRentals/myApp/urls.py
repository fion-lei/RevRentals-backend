from django.urls import path
from .views import *
from .garage_views import *
from .admin_views import *
from .reservations_views import *
from .vehicle_views import GetVIN
from .notifications_views import *
from myApp.vehicle_views import *
from myApp.gear_views import *
from .storage_lot_views import *
import logging

logger = logging.getLogger(__name__)


urlpatterns = [
    # User URLs
    # Profile Login/Register/Details
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/profile-details/', ProfileDetailsView.as_view(), name='profile-details'),
    path('api/profile-details/<int:profile_id>/', ProfileDetailsView.as_view(), name='get-profile-details'),
    path('api/get-profile-id/<str:username>/', GetProfileIDView.as_view(), name='get-profile-id'),
    
    # Marketplace
    path('api/motorized-vehicles/', ViewAllMotorizedVehicles.as_view(), name='view-all-motorized-vehicles'),
    path('api/motorized-vehicles/<str:vin>/',ViewMaintenanceRecords.as_view(), name = 'view-maintenance-records'),
    path('api/storage-lots/', ViewAllStorageLots.as_view(), name='view-all-storage-lots'),
    path('api/gear-items/', ViewAllGearItems.as_view(), name='view-all-gear-items'),

    #date details
    path('api/reserved_dates_motorcycle/<str:vin>/', ReservedDatesView.as_view(), name='view-motorcycle-dates'),
    
    # Reservations for items
    path('api/add-reservation/', AddReservationView.as_view(), name='add-reservation'),
    
    # Agreements and Transactions
    path('api/add-agreement/', AddAgreementView.as_view(), name='add-agreement'),
    path('api/add-transaction/', AddTransactionView.as_view(), name='add-transaction'),
    path('api/get-agreement/<int:reservation_no>/', GetAgreementView.as_view(), name='get-agreement'),
    path('api/get-transaction/<int:reservation_no>/', GetTransactionView.as_view(), name='get-transaction'),
    path('api/view-reservation-details/<int:reservation_no>/', ViewReservationDetails.as_view(), name='view-reservation-details'),
    
    # Garage
    path('api/get-garage-id/<int:profile_id>/', GetGarageIDView.as_view(), name='get_garage_id'),
    path('api/add-listing/', AddMotorizedVehicleView.as_view(), name='add-listing'),
    path('api/add-gear-listing/', AddGearView.as_view(), name = 'add-gear'),
    path('api/view-listing/', ViewAllGarageItemsView.as_view(), name='view-listing'),
    path('api/add-maintenance-records/', AddMaintenanceRecordsView.as_view(), name='add-maintenance-records'),
    path('api/update-rental-price/', UpdateRentalPriceViews.as_view(), name='update-rental-price'),
    path('api/rentals/buyer/<int:buyer_id>/', BuyerRentalHistoryView.as_view(), name='buyer-rental-history'),
    
    
    # Admin URLs
    path('api/admin-login/', AdminLoginView.as_view(), name='admin-login'),
    path('api/get-admin-id/', GetAdminIDView.as_view(), name='get-admin-id'),
    # Agreements, Reservations, Transactions
    path('api/reservations/', ViewAllReservations.as_view(), name ='view-reservations'),
    path('api/get-transaction/<int:reservation_no>/', GetTransactionView.as_view(), name = 'get-transaction' ),

    
    # Lots
    path('api/add-lot-listing/',AddLotListing.as_view(), name = 'add-lot-listing'),
    path('api/edit-lot-listing/<int:lot_no>/',EditLotListing.as_view(), name = 'edit-lot-listing'),
    path('api/lot-rental/check/<int:profile_id>/', CheckActiveLotRentalView.as_view(), name='check-active-lot-rental'),
    path('get-all-lots/', GetLotsView.as_view(), name='get-all-lots'), # for sorting

    # notifications / reservations
    path('api/notifications/seller/<int:seller_id>/', SellerNotificationsView.as_view(), name='seller-notifications'),
    path('api/notifications/buyer/<int:buyer_id>/', BuyerNotificationsView.as_view(), name='buyer-notifications'),
    path('api/reservations/<int:reservation_no>/', UpdateReservationView.as_view(), name='update-reservation'),
    path('api/notifications/delete/<int:reservation_no>/', DeleteReservationView.as_view(), name='delete-reservation'),
    path('api/notifications/check/<int:profile_id>/', CheckNotificationsView.as_view(), name='check-notifications'),
    
    # Vehicle filtering
    path('filter-by-multiple-conditions/', SearchByMultipleConditionsView.as_view(), name='filter-by-multiple-conditions'),
    path('get-all-vehicles/', GetVehiclesView.as_view(), name='get-all-vehicles'),    
    
    # Gear filtering
    path('filter-gear-by-multiple-conditions/', SearchGearByMultipleConditionsView.as_view(), name='filter-gear-by-multiple-conditions'),
    path('get-all-gear/', GetAllGearView.as_view(), name='get-all-gear'),
]
