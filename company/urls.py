from django.urls import path
from . import views

urlpatterns = [
    path('new', views.create_company, name='create_company'),
    path('settings', views.company_settings, name='company_settings'),
    path('savecompany', views.save_company_name),
    path('edit', views.edit_company, name='edit_company'),
    path('subscription', views.view_subscription, name='subscription'),
    path('customers', views.customer_dashboard, name='customer_dashboard'),
    path('customers/new', views.new_customer, name='new_customer'),
    path('customers/info/<int:customer_id>', views.each_customer),
    path('customers/edit/<int:customer_id>', views.edit_customer),
    path('customers/delete/<int:customer_id>', views.delete_customer),
    path('customers/download', views.download_customers, name='download_customers'),
    path('shipping-carriers', views.shipping_carriers_dashboard, name='shipping_carriers_dashboard'),
    path('shipping-carriers/new', views.new_shipping_carrier, name='new_shipping_carrier'),
    path('shipping-carriers/info/<int:shipping_id>', views.each_shipping_carrier),
    path('shipping-carriers/edit/<int:shipping_id>', views.edit_shipping_carrier),
    path('shipping-carriers/delete/<int:shipping_id>', views.delete_shipping_carrier),
    path('shipping-carriers/download', views.download_shipping_carriers, name='download_shipping_carriers')
]
