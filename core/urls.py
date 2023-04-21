from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authentication import views as user_views

urlpatterns = [    
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')), 
    path('', include('data.urls')),
    path('crypto/', include('app_crypto.urls')),
    path('dalys/', include('app_dalys.urls')),
    path('water/', include('app_water.urls')),
    path('front/', include('app_front.urls')),
    path('helpdesk/', include('helpdesk.urls')),
    path('', include('app_front.urls')),
    path('', include('app.urls')),    
]