from django.db.models import Avg
from django.utils.timezone import make_aware
from datetime import time, datetime
from .forms import IngresoTokensForm
from .models import IngresoTokens
from promedio.models import Promedio  # ✅ Correcto
from django.shortcuts import render
import pytz

def registrar_tokens(request):
    id_studio = request.session.get('id_studio')
    print("id_estudio (modelo):", id_studio)
    mensaje = None

    if request.method == 'POST':
        print("Formulario enviado")
        form = IngresoTokensForm(request.POST, studio_id=id_studio)
        if form.is_valid():
            modelo = form.cleaned_data['id_modelo']
            print("id_modelo (modelo):", modelo)
            print("id_modelo id (modelo.id):", modelo.id) 
            fecha = form.cleaned_data['fecha']

            # Calcular rango del día completo
            colombia_tz = pytz.timezone('America/Bogota')
            inicio = make_aware(datetime.combine(fecha, time.min), colombia_tz)
            fin = make_aware(datetime.combine(fecha, time.max), colombia_tz)

            # Consultar promedios de ese día
            promedios = Promedio.objects.filter(
                id_modelo=modelo,
                id_studio=id_studio,
                fecha__range=(inicio, fin)
            ).aggregate(
                promedio_posicion=Avg('promedio'),
                usuarios=Avg('users')
            )

            # Guardar o actualizar
            ingreso, creado = IngresoTokens.objects.update_or_create(
                id_modelo=modelo,
                id_studio=id_studio,
                fecha=fecha,
                defaults={
                    'token_cb': form.cleaned_data['token_cb'],
                    'token_otro': form.cleaned_data['token_otro'],
                    'promedio_posicion': promedios['promedio_posicion'] or 0,
                    'usuarios': promedios['usuarios'] or 0,
                }
            )

            mensaje = "¡Guardado correctamente!" if creado else "¡Actualizado correctamente!"

        else:
            print("Errores del formulario:", form.errors)
    else:
        form = IngresoTokensForm(studio_id=id_studio)

    return render(request, 'ingresos_tokens/registro_tokens.html', {'form': form, 'mensaje': mensaje})
