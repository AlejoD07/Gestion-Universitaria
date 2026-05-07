from django.urls import path
from . import views

urlpatterns = [

    # Inicio
    path('', views.inicio, name='contabilidad_inicio'),

    # Nóminas
    path('nominas/', views.lista_nominas, name='lista_nominas'),
    path('nominas/crear/', views.crear_nomina, name='crear_nomina'),
    path('nominas/editar/<int:id>/', views.editar_nomina, name='editar_nomina'),
    path('nominas/eliminar/<int:id>/', views.eliminar_nomina, name='eliminar_nomina'),

    # Presupuestos
    path('presupuestos/', views.lista_presupuestos, name='lista_presupuestos'),
    path('presupuestos/crear/', views.crear_presupuesto, name='crear_presupuesto'),
    path('presupuestos/editar/<int:id>/', views.editar_presupuesto, name='editar_presupuesto'),
    path('presupuestos/eliminar/<int:id>/', views.eliminar_presupuesto, name='eliminar_presupuesto'),

    # Ingresos
    path('ingresos/', views.lista_ingresos, name='lista_ingresos'),
    path('ingresos/crear/', views.crear_ingreso, name='crear_ingreso'),
    path('ingresos/eliminar/<int:id>/', views.eliminar_ingreso, name='eliminar_ingreso'),
]
