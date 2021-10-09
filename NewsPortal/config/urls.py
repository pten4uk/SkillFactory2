from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('newspaper.urls')),
    path('accounts/', include('allauth.urls')),
]
