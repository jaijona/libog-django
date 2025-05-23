from django.urls import path
from . import views

urlpatterns = [
    path('mostrar_datos/', views.mostrar_datos, name='mostrar_datos'),
    path('actualizar/', views.actualizar_tabla, name='actualizar_tabla'),
]
