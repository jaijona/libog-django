from django.urls import path
from . import views

urlpatterns = [
    path('registro_tokens/', views.registrar_tokens, name='registrar_tokens'),
]
