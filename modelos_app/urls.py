# modelos/urls.py
from django.urls import path
from . import views

urlpatterns = [
                path('registro_modelos/', views.registro_modelos, name='registro_modelos'),

]

