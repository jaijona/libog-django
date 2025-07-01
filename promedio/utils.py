import requests
import json
from datetime import datetime
import pytz

from django.db import connection  # ✅ Importar esto
from modelos_app.models import ModeloRegistrado
from promedio.models import Promedio,DataAllUseStr

def guardar_promedios():
    url = "https://chaturbate.com/affiliates/api/onlinerooms/?format=json&wm=zXPBe"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("Error al consultar la API")
            return

        data = json.loads(response.text)



        # Zona horaria Colombia
        colombia_tz = pytz.timezone("America/Bogota")
        ahora = datetime.now(colombia_tz)
        hora_actual = ahora.replace(minute=0, second=0, microsecond=0)

        # Contadores
        total = len(data)
        fem = sum(1 for m in data if m.get("gender") == "f")
        male = sum(1 for m in data if m.get("gender") == "m")
        tra = sum(1 for m in data if m.get("gender") == "s")
        cou = sum(1 for m in data if m.get("gender") == "c")

        users_all = sum(m.get("num_users", 0) for m in data)
        users_fem = sum(m.get("num_users", 0) for m in data if m.get("gender") == "f")
        users_male = sum(m.get("num_users", 0) for m in data if m.get("gender") == "m")
        users_tra = sum(m.get("num_users", 0) for m in data if m.get("gender") == "s")
        users_cou = sum(m.get("num_users", 0) for m in data if m.get("gender") == "c")

        # Ver si ya hay registro en esa hora
        registro_existente = DataAllUseStr.objects.filter(fecha=hora_actual).first()
        print("Guardando con fecha:", hora_actual)
        if registro_existente:
            nuevo_contador = registro_existente.contador + 1

            # Promediar STREAMS
            registro_existente.strea_all = ((registro_existente.strea_all * registro_existente.contador) + total) / nuevo_contador
            registro_existente.strea_fem = ((registro_existente.strea_fem * registro_existente.contador) + fem) / nuevo_contador
            registro_existente.strea_male = ((registro_existente.strea_male * registro_existente.contador) + male) / nuevo_contador
            registro_existente.strea_tra = ((registro_existente.strea_tra * registro_existente.contador) + tra) / nuevo_contador
            registro_existente.strea_cou = ((registro_existente.strea_cou * registro_existente.contador) + cou) / nuevo_contador

            # Promediar USERS
            registro_existente.users_all = ((registro_existente.users_all * registro_existente.contador) + users_all) / nuevo_contador
            registro_existente.users_fem = ((registro_existente.users_fem * registro_existente.contador) + users_fem) / nuevo_contador
            registro_existente.users_male = ((registro_existente.users_male * registro_existente.contador) + users_male) / nuevo_contador
            registro_existente.users_tra = ((registro_existente.users_tra * registro_existente.contador) + users_tra) / nuevo_contador
            registro_existente.users_cou = ((registro_existente.users_cou * registro_existente.contador) + users_cou) / nuevo_contador

            registro_existente.contador = nuevo_contador
            registro_existente.save()

        else:
            # Crear nuevo registro si no existe
            DataAllUseStr.objects.create(
                fecha=hora_actual,
                strea_all=total,
                strea_fem=fem,
                strea_male=male,
                strea_tra=tra,
                strea_cou=cou,

                users_all=users_all,
                users_fem=users_fem,
                users_male=users_male,
                users_tra=users_tra,
                users_cou=users_cou,
                contador=1
            )



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
                        print("Guardando con fechat:", hora_actual)
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
