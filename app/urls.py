from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('auth/', include('core.urls')),
    path('api/v1/expenses/', include('expenses.urls')),
    path('admin/', admin.site.urls),
]
