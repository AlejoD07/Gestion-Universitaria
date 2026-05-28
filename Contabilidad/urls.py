from django.urls import path
from . import views

urlpatterns = [

    # Inicio
    path('', views.inicio, name='contabilidad_inicio'),

    # Nóminas
    path('nominas/', views.lista_nominas, name='lista_nominas'),
    path('nominas/importar/', views.simular_importacion_nomina, name='simular_importacion_nomina'),
    path('nominas/lotes/<int:id>/', views.detalle_lote_nomina, name='detalle_lote_nomina'),
    path('nominas/lotes/<int:id>/validar/', views.validar_lote_nomina, name='validar_lote_nomina'),
    path('nominas/lotes/<int:id>/contabilizar/', views.contabilizar_lote_nomina, name='contabilizar_lote_nomina'),
    path('nominas/crear/', views.crear_nomina, name='crear_nomina'),
    path('nominas/buscar-empleado/', views.buscar_empleado_nomina, name='buscar_empleado_nomina'),
    path('nominas/editar/<int:id>/', views.editar_nomina, name='editar_nomina'),
    path('nominas/eliminar/<int:id>/', views.eliminar_nomina, name='eliminar_nomina'),

    # Presupuestos
    path('presupuestos/', views.lista_presupuestos, name='lista_presupuestos'),
    path('presupuestos/plan/crear/', views.crear_plan_presupuestal, name='crear_plan_presupuestal'),
    path('presupuestos/plan/demo/', views.crear_plan_presupuestal_demo, name='crear_plan_presupuestal_demo'),
    path('presupuestos/plan/<int:id>/', views.detalle_plan_presupuestal, name='detalle_plan_presupuestal'),
    path('presupuestos/plan/<int:plan_id>/partida/crear/', views.crear_partida_presupuestal, name='crear_partida_presupuestal'),
    path('presupuestos/plan/<int:plan_id>/revision/', views.registrar_revision_presupuestal, name='registrar_revision_presupuestal'),
    path('presupuestos/partida/<int:partida_id>/ajuste/', views.registrar_ajuste_presupuestal, name='registrar_ajuste_presupuestal'),
    path('presupuestos/crear/', views.crear_presupuesto, name='crear_presupuesto'),
    path('presupuestos/editar/<int:id>/', views.editar_presupuesto, name='editar_presupuesto'),
    path('presupuestos/eliminar/<int:id>/', views.eliminar_presupuesto, name='eliminar_presupuesto'),

    # Ingresos
    path('ingresos/', views.lista_ingresos, name='lista_ingresos'),
    path('ingresos/crear/', views.crear_ingreso, name='crear_ingreso'),
    path('ingresos/eliminar/<int:id>/', views.eliminar_ingreso, name='eliminar_ingreso'),

    path('areas-contables/', views.lista_areas_contables, name='lista_areas_contables'),
    path('areas-contables/crear/', views.crear_area_contable, name='crear_area_contable'),
    path('areas-contables/estado/<int:id>/', views.cambiar_estado_area_contable, name='cambiar_estado_area_contable'),
]
