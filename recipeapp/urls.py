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
    path('personalinfo', views.getPersonalInfo, name='personalinfo'),
    path('personalinfo/edit', views.UpdateContactInfo.as_view(), name='contactInfo'),
    path('personalinfo/change_password', views.updatePassword, name='change_password'),
    path('personalinfo/change_email', views.UpdateEmail.as_view(), name='change_email'),
    path('feedback', views.user_feedback, name='feedback'),
    path('forget-password', views.forget_password, name='forget-password'),
    path('update-password/<token>', views.update_password, name='update-password')
]
