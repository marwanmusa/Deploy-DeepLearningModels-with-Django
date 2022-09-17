from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from trafficsign_classifier_web import views
urlpatterns = [
    path('admin/', admin.site.urls),

    # add these to configure our home page (default view) and result web page
    path('', views.result, name='home'),
    # path('result/', views.result, name='result'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)