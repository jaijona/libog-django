"""
URL configuration for sistema_login project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# sistema_login/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),  # 👈 Esto importa las rutas de la app
    path('', include('modelos_app.urls')),        # rutas para modelos registrados
    path('', include('posicion.urls')), #cuadro de informacion
    path('', include('promedio.urls')), #promedio
    path('', include('monitores.urls')), #promedio
    path('', include('ingresos_tokens.urls')), #promedio
    
    
]

