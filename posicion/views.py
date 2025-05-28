
"""
import requests
import json
import pandas as pd
from django.shortcuts import render
from modelos_app.models import ModeloRegistrado as informacion
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import render
from usuarios.utils import login_requerido

def obtener_modelos_deseados(id_login):
    return informacion.objects.filter(estado=1, studio_id=id_login).values_list('usuario', flat=True)
    

def obtener_datos_filtrados(id_login):
    #modelos_deseados = set(obtener_modelos_deseados(id_login))
    #modelos_deseados = set(u.lower().strip() for u in obtener_modelos_deseados(id_login))
    #url = "https://chaturbate.com/affiliates/api/onlinerooms/?format=json&wm=zXPBe"
    
    try:
        modelos_deseados = set(u.lower().strip() for u in obtener_modelos_deseados(id_login))
        url = "https://chaturbate.com/affiliates/api/onlinerooms/?format=json&wm=zXPBe"
        respuesta = requests.get(url)

        respuesta = requests.get(url)
        if respuesta.status_code != 200:
            print("Error al acceder a la API, código:", respuesta.status_code)
            return pd.DataFrame(), 0, 0

        datos = json.loads(respuesta.text)
        print(f"Total modelos recibidos de API: {len(datos)}")
        if datos:
            print(json.dumps(datos[0], indent=2))  # 👈 Verifica cómo luce un modelo
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
        return pd.DataFrame(), 0, 0


@login_requerido
def mostrar_datos(request):
    id_login = int(request.GET.get('id_login', 1))
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
@login_requerido
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
"""
import requests
import json
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from modelos_app.models import ModeloRegistrado as informacion
from usuarios.utils import login_requerido

# ✅ Obtener los nombres de usuario de modelos activos en el estudio
def obtener_modelos_deseados(id_login):
    return informacion.objects.filter(estado=1, studio_id=id_login).values_list('usuario', flat=True)

# ✅ Obtener datos de la API y filtrar solo los modelos deseados
def obtener_datos_filtrados(id_login):
    try:
        modelos_deseados = set(u.lower().strip() for u in obtener_modelos_deseados(id_login))
        print("Modelos deseados desde BD:", modelos_deseados)

        url = "https://chaturbate.com/affiliates/api/onlinerooms/?format=json&wm=zXPBe"
        respuesta = requests.get(url)

        if respuesta.status_code != 200:
            print("❌ Error al acceder a la API. Código:", respuesta.status_code)
            return pd.DataFrame(), 0, 0

        datos = json.loads(respuesta.text)
        print(f"✅ Total modelos recibidos desde la API: {len(datos)}")

        if datos:
            print("🔍 Ejemplo de modelo desde API:")
            print(json.dumps(datos[0], indent=2))

        filtrados = []
        for idx, modelo in enumerate(datos):
            username_api = modelo.get('username', '').lower().strip()

            if username_api in modelos_deseados:
                print("✅ MATCH:", modelo['username'])
                filtrados.append({
                    'Posicion': idx,
                    'Modelo': modelo['username'],
                    'Estado': modelo.get('current_show', 'unknown'),
                    'Usuarios': modelo.get('num_users', 0),
                    'Seguidores': modelo.get('num_followers', 0),
                    'Online': round(modelo.get('seconds_online', 0) / 60, 1),
                    'Tags': ', '.join(modelo.get('tags', [])),
                })
            #else:
                #print("❌ NO MATCH:", modelo['username'])

        num_modelos = len(datos)
        total_usuarios = sum(m.get('num_users', 0) for m in datos)

        return pd.DataFrame(filtrados), num_modelos, total_usuarios

    except Exception as e:
        print("❗ Error al procesar datos de la API:", e)
        return pd.DataFrame(), 0, 0

# ✅ Vista principal que muestra los datos
@login_requerido
def mostrar_datos(request):
    id_login = request.session.get('usuario_id')
    df, num_modelos, total_usuarios = obtener_datos_filtrados(id_login)
    print("🔍 ID de login recibido:", id_login)

    context = {
        'modelos': df.to_dict(orient='records'),
        'total_modelos': num_modelos,
        'total_usuarios': total_usuarios,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('posicion/tabla_modelos.html', context, request=request)
        return JsonResponse({'html': html})

    return render(request, 'posicion/mostrar_datos.html', context)

# ✅ Vista usada para actualizar la tabla dinámicamente
@login_requerido
def actualizar_tabla(request):
    id_login = request.session.get('usuario_id')
    df, num_modelos, total_usuarios = obtener_datos_filtrados(id_login)

    context = {
        'modelos': df.to_dict(orient='records'),
        'total_modelos': num_modelos,
        'total_usuarios': total_usuarios,
    }

    html = render_to_string('posicion/tabla_modelos.html', context)
    return JsonResponse({'html': html})
