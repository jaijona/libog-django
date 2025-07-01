import os
import django
from datetime import datetime

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_login.settings')  # 👈 reemplaza esto con el nombre real de tu proyecto
django.setup()

# Importa la función desde utils.py
from promedio.utils import guardar_promedios

print(f"⏳ Ejecutando tarea a las {datetime.now()}")
guardar_promedios()
print("✅ Tarea completada")
