from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views


urlpatterns = [
   path('register/',views.register),
   path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('logout_view/',views.logout_view),
   path('getorder/',views.getorder),
   path('getService/',views.getService),
   path('getRating/',views.getRating),
   path('Notification/',views.getNotification),
   path('getorder_id/<int:id>',views.getorder_id),
   path('getService_id/<int:id>',views.getService_id),
   path('getRating_id/<int:id>',views.getRating_id),
   path('getNotification_id/<int:id>',views.getNotification_id),
   path('createOrder/',views.createOrder),
   path('createService/',views.createService),
   path('addRating/',views.addRating),
   path('updateOrder/<int:id>',views.updateOrder),
   path('deleteOrder/<int:id>',views.deleteOrder),

]
