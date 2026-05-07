from django.urls import path
from . import views

app_name = "rrhh"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('inicio/', views.inicio, name='inicio'),
    path('crear_empleado/', views.crear_empleado, name='crear_empleado'),
    path('editar_empleado/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'),
    path('actualizar_empleado/<int:empleado_id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('eliminar_empleado/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'),
    #areas
    path('areas/', views.areas, name='areas'),
    path('editar_area/<int:area_id>/', views.editar_area, name='editar_area'),
    path('agregar_area/', views.agregar_area, name='agregar_area'),
    path('eliminar_area/<int:area_id>/', views.eliminar_area, name='eliminar_area'),
    #novedades
    path('novedades/<int:empleado_id>/', views.novedades, name='novedades'),
    path('agregar_novedad/', views.agregar_novedad, name='agregar_novedad'),
    #certificado
    path('certificado_laboral/<int:empleado_id>/', views.certificado_laboral, name='certificado_laboral'),
]

