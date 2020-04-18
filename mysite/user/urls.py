from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

app_name='user'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('all/',views.all,name='all'),
    path('frontcam/',views.front_cam,name='frontcam'),
    path('cam/',views.cam,name='cam')
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

