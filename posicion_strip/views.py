import requests
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from modelos_app.models import ModeloRegistrado as data_models
from usuarios.utils import login_requerido
from datetime import datetime

# ✅ Obtener los nombres de usuario de modelos activos en el estudio (usuario_strip)
def obtener_modelos_stripchat(id_studio):
    return data_models.objects.filter(estado=1, studio_id=id_studio).values_list('usuario_strip', flat=True)

# ✅ Obtener datos de la API de Stripchat y filtrar
def obtener_datos_stripchat(id_studio):
    try:
        todos = obtener_modelos_stripchat(id_studio)
        descartados = [u for u in todos if not u]
        print("⚠️ Modelos ignorados por usuario_strip vacío o None:", descartados)

        nombres_deseados = set(
            u.lower().strip()
            for u in todos
            if u
        )
        print("🔍 Modelos deseados:", nombres_deseados)


        #nombres_deseados = set(u.lower().strip() for u in obtener_modelos_stripchat(id_studio))
        print("🔍 Modelos deseados:", nombres_deseados)

        url = "https://es.stripchat.com/api/front/models"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://stripchat.com/"
        }

        encontrados = []
        limit = 99
        offset = 0
        posicion_global = 0

        while True:
            params = {
                "limit": limit,
                "offset": offset,
                "primaryTag": "girls",
                "removeShows": "true"
            }

            response = requests.get(url, params=params, headers=headers)
            if response.status_code != 200:
                print(f"❌ Error al acceder a Stripchat. Código: {response.status_code}")
                break

            data = response.json().get("models", [])
            if not data:
                break
            """
            for model in data:
                posicion_global += 1
                username_raw = model.get("username")
                username = username_raw.lower().strip() if username_raw else ""
                if username and username in nombres_deseados:
                    encontrados.append({
                        "Posicion": posicion_global,
                        "Modelo": model.get("username"),
                        "Usuarios": model.get("viewersCount", 0),
                        "HD": model.get("isHd", False),
                        "Estado": model.get("status", "desconocido"),
                        "Género": model.get("broadcastGender", "N/A")
                    })
            """

            for model in data:
                posicion_global += 1

                username_raw = model.get("username")
                if not username_raw:  # Ignora si es None, vacío o False
                    continue
                if not username_raw:
                    print("⚠️ Modelo ignorado por username vacío o None:", model)
                    continue
                
                nombres_deseados = set(
                   u.lower().strip()
                    for u in obtener_modelos_stripchat(id_studio)
                    if u  # esto filtra None, "", 0, etc.
                )


                username = username_raw.lower().strip()
                if username in nombres_deseados:
                    encontrados.append({
                        "Posicion": posicion_global,
                        "Modelo": username_raw,
                        "Usuarios": model.get("viewersCount", 0),
                        "HD": model.get("isHd", False),
                        "Estado": model.get("status", "desconocido"),
                        "Género": model.get("broadcastGender", "N/A")
                    })


            if len(encontrados) == len(nombres_deseados):
                break
            offset += limit

        total_modelos = posicion_global
        total_usuarios = sum(m["Usuarios"] for m in encontrados)
        hora_actualizacion = datetime.now()

        return pd.DataFrame(encontrados), total_modelos, total_usuarios, hora_actualizacion

    except Exception as e:
        print("❗ Error procesando Stripchat:", e)
        return pd.DataFrame(), 0, 0, datetime.now()

# ✅ Vista principal adaptada a Stripchat
@login_requerido
def mostrar_datos_stripchat(request):
    id_studio = request.session.get("id_studio")
    df, num_modelos, total_usuarios, hora_actualizacion = obtener_datos_stripchat(id_studio)

    context = {
        "modelos": df.to_dict(orient="records"),
        "total_modelos": num_modelos,
        "total_usuarios": total_usuarios,
        "hora_actualizacion": hora_actualizacion.time()
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("posicion_strip/tabla_modelos_stripchat.html", context, request=request)
        return JsonResponse({"html": html})

    return render(request, "posicion_strip/mostrar_datos_stripchat.html", context)

# ✅ Vista para actualizar AJAX
@login_requerido
def actualizar_tabla_stripchat(request):
    id_studio = request.session.get("id_studio")
    df, num_modelos, total_usuarios, hora_actualizacion = obtener_datos_stripchat(id_studio)

    context = {
        "modelos": df.to_dict(orient="records"),
        "total_modelos": num_modelos,
        "total_usuarios": total_usuarios,
        "hora_actualizacion": hora_actualizacion.time()
    }

    html = render_to_string("posicion_strip/tabla_modelos_stripchat.html", context)
    return JsonResponse({"html": html})
