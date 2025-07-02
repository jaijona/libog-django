from django.urls import path
from .views import ver_promedios,exportar_excel
from .views import api_guardar_promedios
from .views import graficas_modelo
from .views import ejecutar_guardar_promedios
from . import views
urlpatterns = [
    path('ver_promedios/', ver_promedios, name='ver_promedios'),
    path('exportar_excel/', exportar_excel, name='exportar_excel'),
    path('api/guardar-promedios/', api_guardar_promedios),
    path('graficas/', graficas_modelo, name='graficas_modelo'),
    path('api/datos-dia/', views.obtener_datos_dia, name='api_datos_dia'),
    path('api/datos-semana/', views.obtener_datos_semana, name='api_datos_semana'),
    path('api/tokens-dia/', views.tokens_por_dia, name='tokens_por_dia'),
    path('api/tokens-semana/', views.tokens_semana_view, name='tokens_semana'),
    path("cron/guardar_promedios/", ejecutar_guardar_promedios),

]
