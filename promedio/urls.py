from django.urls import path
from .views import ver_promedios,exportar_excel

urlpatterns = [
    path('ver_promedios/', ver_promedios, name='ver_promedios'),
    path('exportar_excel/', exportar_excel, name='exportar_excel'),
]
