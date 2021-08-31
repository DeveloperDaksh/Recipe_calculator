from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('login/', views.login_user, name='login'),
    path('register/', views.create_user, name='register'),
    path('about/', views.about_us, name='about_us'),
    path('help/', views.help_us, name='help_us'),
    path('contact', views.contact_us, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
]
