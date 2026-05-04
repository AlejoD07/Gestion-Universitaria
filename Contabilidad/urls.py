from django.urls import path
from . import views

urlpatterns = [
    path('nomina/detalle/', views.detalle_nomina, name='detalle_nomina'),
]
