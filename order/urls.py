from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('register/', views.register_view, name='register'), 
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='change_password.html',
        success_url='login/'
    ), name='change_password'), 
    #forget password
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html' ),
         name='password_reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
     
     
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('services/', views.service_list, name='service_list'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('order/<int:service_id>/', views.create_order, name='create_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('update-order/<int:order_id>/', views.update_order, name='update_order'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/update-order/<int:order_id>/', views.admin_update_order, name='admin_update_order'),
    path('rate-check/<int:order_id>/', views.check_rating_permission, name='check_rating_permission'),
    path('orders/<int:order_id>/rate/', views.add_rating, name='add_rating'),
    path('orders_to_users/',views.orders_to_user, name='orders_to_user'),
    path('notifications/', views.user_notifications, name='user_notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),












        
      
       

]
