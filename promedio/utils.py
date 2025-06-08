import requests
import json
from datetime import datetime
import pytz

from django.db import connection  # ✅ Importar esto
from modelos_app.models import ModeloRegistrado
from promedio.models import Promedio

def guardar_promedios():
    url = "https://chaturbate.com/affiliates/api/onlinerooms/?format=json&wm=zXPBe"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("Error al consultar la API")
            return

        data = json.loads(response.text)
        studio_ids = ModeloRegistrado.objects.values_list('studio_id', flat=True).distinct()

        for studio_id in studio_ids:
            modelos_deseados = ModeloRegistrado.objects.filter(estado=1, studio_id=studio_id)
            usernames = set(modelos_deseados.values_list('usuario', flat=True))

            for idx, modelo in enumerate(data):
                username = modelo['username']
                if username in usernames:
                    try:
                        modelo_registrado = modelos_deseados.get(usuario=username)
                        colombia_tz = pytz.timezone('America/Bogota')
                        #hoy = datetime.now(colombia_tz)
                        ahora = datetime.now(colombia_tz)

                        # Redondear al inicio de la hora
                        hora_actual = ahora.replace(minute=0, second=0, microsecond=0)

                        users_count = modelo.get("num_users", 0)

                        # Filtro exacto por hora
                        promedio_existente = Promedio.objects.filter(
                            id_modelo=modelo_registrado,
                            id_studio=studio_id,
                            fecha=hora_actual
                        ).first()

                        if promedio_existente:
                            nuevo_contador = promedio_existente.contador + 1

                            nuevo_promedio = (
                                (promedio_existente.promedio * promedio_existente.contador) + idx
                            ) / nuevo_contador

                            nuevo_users = (
                                (promedio_existente.users * promedio_existente.contador) + users_count
                            ) / nuevo_contador

                            promedio_existente.promedio = nuevo_promedio
                            promedio_existente.users = nuevo_users
                            promedio_existente.contador = nuevo_contador
                            promedio_existente.save()
                        else:
                            # Si no existe, lo creamos por primera vez
                            Promedio.objects.create(
                                id_modelo=modelo_registrado,
                                id_studio=studio_id,
                                promedio=idx,
                                users=users_count,
                                contador=1,
                                fecha=hora_actual
                            )
                    except ModeloRegistrado.DoesNotExist:
                        continue

        print("Promedios guardados/actualizados correcta.")

    except Exception as e:
        print(f"Error al guardar promedios: {str(e)}")

    finally:
        # ✅ Cerrar la conexión pase lo que pase
        connection.close()
