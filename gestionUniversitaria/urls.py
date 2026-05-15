from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='home_general'),
    path('login/', views.login_view, name='login'),
    path('salir/', views.logout_view, name='logout'),
    path('sin-permiso/', views.sin_permiso, name='sin_permiso'),
    path('rrhh/', include('RecursosHumanos.urls')),
    path('academica/', include('gestionAcademica.urls')),
    path('contabilidad/', include('Contabilidad.urls')),
    path('solicitudes/', include('solicitudes.urls')),
    path('inventario/', include('inventario.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
