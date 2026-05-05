from django.urls import path
from . import views

app_name = "inventario"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('categorias/', views.categorias, name='categorias'),
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path('guardar_categoria/', views.guardar_categoria, name='guardar_categoria'),
    path('actualizar_categoria/<int:id>/', views.actualizar_categoria, name='actualizar_categoria'),
    path('eliminar_categoria/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('items/', views.items, name='items'),
    path('crear_item/', views.crear_item, name='crear_item'),
    path('guardar_item/', views.guardar_item, name='guardar_item'),
    path('actualizar_item/<int:id>/', views.actualizar_item, name='actualizar_item'),
    path('eliminar_item/<int:id>/', views.eliminar_item, name='eliminar_item'),
    path('prestamos/', views.prestamos, name='prestamos'),
    path('crear_prestamo/', views.crear_prestamo, name='crear_prestamo'),
    path('guardar_prestamo/', views.guardar_prestamo, name='guardar_prestamo'),
    path('actualizar_prestamo/<int:id>/', views.actualizar_prestamo, name='actualizar_prestamo'),
    path('eliminar_prestamo/<int:id>/', views.eliminar_prestamo, name='eliminar_prestamo'),
    path('lista_inventario/', views.lista_inventario, name='lista_inventario')
]