# usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_usuario, name='login'),
    path('inicio/', views.inicio, name='inicio'),
    path('logout/', views.logout_usuario, name='logout'),
    #path('registro_modelos/', views.registro_modelos, name='registro_modelos'),
    path('tabla_posiciones/', views.tabla_posiciones, name='tabla_posiciones'),
]
