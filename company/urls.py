from django.urls import path
from . import views

urlpatterns = [
    path('new', views.create_company, name='create_company'),
    path('settings', views.company_settings, name='company_settings'),
    path('savecompany', views.save_company_name),
    path('edit', views.edit_company, name='edit_company'),
    path('subscription', views.view_subscription, name='subscription')
]
