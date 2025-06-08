
from django.db.models.functions import TruncDate
from django.db.models import Avg, DateField
from datetime import datetime
from usuarios.utils import login_requerido
from .models import Promedio
from django.shortcuts import render
from django.core.paginator import Paginator
from modelos_app.models import ModeloRegistrado
import openpyxl
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.http import JsonResponse
from promedio.utils import guardar_promedios 

import os


CLAVE_SECRETA = os.getenv("CLAVE_SECRETA")

def api_guardar_promedios(request):
    key = request.GET.get("key")

    if key != CLAVE_SECRETA:
        return JsonResponse({"error": "No autorizado"}, status=403)

    try:
        guardar_promedios()
        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    



@login_requerido
def ver_promedios(request):
    id_studio = request.session.get('id_studio')
    print("studio_id:", id_studio)  # ← Esto ahora debe aparecer
    datos = Promedio.objects.filter(id_studio=id_studio,id_modelo__estado=1).select_related('id_modelo')

    # Obtener filtros
    fecha_filtro = request.GET.get('fecha')
    usuario_filtro = request.GET.get('usuario')
    jornada_filtro = request.GET.get('jornada')
    
    """
    # Aplicar filtro por fecha
    if fecha_filtro:
        try:
            # Convertir el string a date
            colombia_tz = pytz.timezone('America/Bogota')
            fecha_base = datetime.strptime(fecha_filtro, '%Y-%m-%d')

            # Crear rango completo del día con zona horaria
            inicio = make_aware(datetime.combine(fecha_base, time.min),colombia_tz)  # 00:00:00
            fin = make_aware(datetime.combine(fecha_base, time.max),colombia_tz)     # 23:59:59.999999

            # Aplicar el filtro
            datos = datos.filter(fecha__range=(inicio, fin))
        except ValueError:
            pass
    """
    # Aplicar filtro por usuario
    if usuario_filtro:
        datos = datos.filter(id_modelo__usuario=usuario_filtro)

    # Aplicar filtro por jornada
    if jornada_filtro:
        datos = datos.filter(id_modelo__jornada=jornada_filtro)

    # Paginación (15 por página)
    paginator = Paginator(datos.order_by('-fecha'), 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Lista de usuarios para mostrar en el dropdown
    usuarios = ModeloRegistrado.objects.filter(studio_id=id_studio,estado=1).values_list('usuario', flat=True).distinct()
    jornada = ModeloRegistrado.objects.filter(studio_id=id_studio,estado=1).values_list('jornada', flat=True).distinct()

    context = {
        'page_obj': page_obj,
        'usuarios': usuarios,
        'jornada': jornada,
        'fecha_filtro': fecha_filtro or '',
        'usuario_filtro': usuario_filtro or '',
        'jornada_filtro': jornada_filtro or '',
    }
    return render(request, 'ver_promedios.html', context)

def exportar_excel(request):
    id_studio = request.session.get('usuario_id')
    datos = Promedio.objects.filter(id_studio=id_studio,id_modelo__estado=1).select_related('id_modelo')

    # Filtros
    fecha_filtro = request.GET.get('fecha')
    usuario_filtro = request.GET.get('usuario')
    jornada_filtro = request.GET.get('jornada')

    if fecha_filtro:
        try:
            fecha_obj = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
            datos = datos.filter(fecha=fecha_obj)
        except ValueError:
            pass

    if usuario_filtro:
        datos = datos.filter(id_modelo__usuario=usuario_filtro)


    if jornada_filtro:
        datos = datos.filter(id_modelo__jornada=jornada_filtro)

    # Crear workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Promedios"

    # Encabezados
    headers = ['Usuario', 'Jornada', 'Promedio','Usuarios', 'Fecha']
    ws.append(headers)

    for item in datos:
        ws.append([
            item.id_modelo.usuario,
            item.id_modelo.jornada,
            item.promedio,
            item.users,
            item.fecha.strftime('%Y-%m-%d')
        ])

    # Ajustar ancho de columnas
    for i, column in enumerate(ws.columns, 1):
        max_length = max(len(str(cell.value)) for cell in column)
        ws.column_dimensions[get_column_letter(i)].width = max_length + 2

    # Respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=promedios_filtrados.xlsx'
    wb.save(response)
    return response