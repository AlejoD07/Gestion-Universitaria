from django.urls import path
from . import views

app_name = 'solicitudes'

urlpatterns = [
    path('', views.home_redirect),
    path('home/', views.home, name='home'),
    # path('inicio/', views.inicio, name='inicio'),
    path('ejemplo_for/<int:id>/', views.ejemplo_for, name='ejemplo_for'),
    path('ejemplo_if/<int:id>', views.ejemplo_if, name='ejemplo_if'),
    # path('form_registro/', views.view_form_registro, name='form_registro'),
    path('form_quejas/', views.view_form_quejas, name='form_quejas'),
    path('detalle_solicitud/<int:id>/', views.detalle_solicitud, name='detalle_solicitud'),
]
