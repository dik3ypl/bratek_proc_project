from django.conf.urls.static import static
from django.urls import path

from common import settings
from .views import dashboard

urlpatterns = [
                  path('', dashboard, name='dashboard'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
