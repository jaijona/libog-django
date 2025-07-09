import requests
from datetime import datetime
import pytz
from django.db import connection
from modelos_app.models import ModeloRegistrado
from posicion_strip.models import Promedio_strip

def guardar_datos_stripchat():
    try:
        # Obtener estudios únicos
        studio_ids = ModeloRegistrado.objects.values_list('studio_id', flat=True).distinct()

        # Configuración API
        url = "https://es.stripchat.com/api/front/models"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://stripchat.com/"
        }

        # Hora redondeada (zona horaria Colombia)
        colombia_tz = pytz.timezone("America/Bogota")
        ahora = datetime.now(colombia_tz)
        hora_actual = ahora.replace(minute=0, second=0, microsecond=0)

        limit = 99
        offset = 0
        posicion_global = 0
        max_paginas = 50 # máximo de 15 páginas para evitar lentitud

        encontrados = []  # Lista de todos los modelos visibles

        while offset < max_paginas * limit:
            params = {
                "limit": limit,
                "offset": offset,
                "primaryTag": "girls",
                "removeShows": "true"
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                print("❌ Error consultando Stripchat")
                break

            data = response.json().get("models", [])
            if not data:
                break

            for model in data:
                posicion_global += 1
                username = model.get("username")
                if not username:
                    continue
                encontrados.append({
                    "username": username.strip().lower(),
                    "posicion": posicion_global,
                    "usuarios": model.get("viewersCount", 0)
                })

            offset += limit

        if not encontrados:
            print("⚠️ No se encontraron modelos.")
            return

        for studio_id in studio_ids:
            modelos_registrados = ModeloRegistrado.objects.filter(
                estado=1, studio_id=studio_id
            )

            usernames_deseados = {
                m.usuario_strip.strip().lower(): m for m in modelos_registrados if m.usuario_strip
            }

            for modelo_visible in encontrados:
                username = modelo_visible["username"]
                if username in usernames_deseados:
                    modelo_obj = usernames_deseados[username]

                    # Buscar si ya hay un registro para esa hora
                    registro_existente = Promedio_strip.objects.filter(
                        id_modelo=modelo_obj,
                        id_studio=studio_id,
                        fecha=hora_actual
                    ).first()

                    if registro_existente:
                        # Actualizar promedio
                        nuevo_contador = registro_existente.contador + 1
                        nueva_posicion = (
                            (registro_existente.promedio * registro_existente.contador) +
                            modelo_visible["posicion"]
                        ) / nuevo_contador
                        nuevos_usuarios = (
                            (registro_existente.users * registro_existente.contador) +
                            modelo_visible["usuarios"]
                        ) / nuevo_contador

                        registro_existente.promedio = nueva_posicion
                        registro_existente.users = nuevos_usuarios
                        registro_existente.contador = nuevo_contador
                        registro_existente.save()

                    else:
                        # Crear si no existe
                        Promedio_strip.objects.create(
                            id_modelo=modelo_obj,
                            id_studio=studio_id,
                            promedio=modelo_visible["posicion"],
                            users=modelo_visible["usuarios"],
                            fecha=hora_actual,
                            contador=1
                        )

        print("✅ Datos Stripchat guardados correctamente para todos los estudios.")

    except Exception as e:
        print("❗ Error guardando datos Stripchat:", e)

    finally:
        connection.close()
