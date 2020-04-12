from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import intworlduser.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', intworlduser.views.signin, name="signin"),
    path('intworldapp/', include('intworldapp.urls')),
    path('intworlduser/', include('intworlduser.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)