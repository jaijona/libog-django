from django.urls import path
from . import views

urlpatterns = [
    path('mostrar_datos_stripchat/', views.mostrar_datos_stripchat, name='mostrar_datos_stripchat'),
    path('actualizar_tabla_stripchat/', views.actualizar_tabla_stripchat, name='actualizar_tabla_stripchat'),
]
