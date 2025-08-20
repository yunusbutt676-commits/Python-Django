from django.contrib import admin
from django.urls import path, include
from inventory.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name='dashboard'),
    path('api/', include('inventory.api_urls')),
]
