from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import intworlduser.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', intworlduser.views.singup, name="singup"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

