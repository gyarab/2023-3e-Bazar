
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls'), name='homepage'),
    path('profilepage/', include('profilepage.urls'), name='profilepage')
]
