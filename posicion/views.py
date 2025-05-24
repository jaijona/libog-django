import requests
import json
import pandas as pd
from django.shortcuts import render
from modelos_app.models import ModeloRegistrado as informacion
from django.template.loader import render_to_string
from django.http import JsonResponse

def obtener_modelos_deseados(id_login):
    return informacion.objects.filter(estado=1, studio_id=id_login).values_list('usuario', flat=True)

def obtener_datos_filtrados(id_login):
    modelos_deseados = set(obtener_modelos_deseados(id_login))
    url = "https://chaturbate.com/affiliates/api/onlinerooms/?format=json&wm=zXPBe"
    
    try:
        respuesta = requests.get(url)
        if respuesta.status_code != 200:
            return pd.DataFrame()

        datos = json.loads(respuesta.text)
        num_modelos = len(datos)
        total_usuarios = sum(m.get('num_users', 0) for m in datos)
        filtrados = [
            {
                'Posicion': idx,
                'Modelo': modelo['username'],
                'Estado': modelo['current_show'],
                'Usuarios': modelo['num_users'],
                'Seguidores': modelo['num_followers'],
                'Online': round(modelo['seconds_online'] / 60, 1),
                'Tags': ', '.join(modelo['tags'])
            }
            for idx, modelo in enumerate(datos)
            if modelo['username'] in modelos_deseados
        ]

        return pd.DataFrame(filtrados), num_modelos, total_usuarios,

    except Exception as e:
        print("Error al procesar datos de la API:", e)
        return pd.DataFrame()


def mostrar_datos(request):
    id_login = request.GET.get('id_login', 1)
    df, num_modelos, total_usuarios = obtener_datos_filtrados(id_login)

    context = {
        'modelos': df.to_dict(orient='records'),
        'total_modelos': num_modelos,
        'total_usuarios': total_usuarios,
    }

    # Si es una llamada AJAX, devuelve solo el HTML parcial
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('posicion/tabla_modelos.html', context, request=request)
        return JsonResponse({'html': html})

    # Si no es AJAX, renderiza la página completa (útil para pruebas)
    return render(request, 'posicion/mostrar_datos.html', context)

def actualizar_tabla(request):
    id_login = request.GET.get('id_login', 1)
    df, num_modelos, total_usuarios= obtener_datos_filtrados(id_login)

    context = {
        'modelos': df.to_dict(orient='records'),
        'total_modelos': num_modelos,
        'total_usuarios': total_usuarios,
    }
    html = render_to_string('posicion/tabla_modelos.html', context)
    return JsonResponse({'html': html})