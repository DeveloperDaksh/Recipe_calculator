from django.contrib import admin
from django.urls import path, include
from django.urls.conf import re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipeapp.urls')),
    path('recipe/', include('recipesandingredients.urls')),
    path('company/',include('company.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
