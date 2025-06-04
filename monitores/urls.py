# modelos/urls.py
from django.urls import path
from . import views

urlpatterns = [
                path('registro_monitores/', views.registro_monitores, name='registro_monitores'),

]

