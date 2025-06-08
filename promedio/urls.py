from django.urls import path
from .views import ver_promedios,exportar_excel
from .views import api_guardar_promedios

urlpatterns = [
    path('ver_promedios/', ver_promedios, name='ver_promedios'),
    path('exportar_excel/', exportar_excel, name='exportar_excel'),
    path('api/guardar-promedios/', api_guardar_promedios),
]
