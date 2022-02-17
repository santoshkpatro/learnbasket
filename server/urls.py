from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('localadmin/', admin.site.urls),
    path('admin/', include('server.api.admin.urls')),
    path('v1/', include('server.api.v1.urls')),
]
