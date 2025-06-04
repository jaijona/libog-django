from django.shortcuts import render, redirect, get_object_or_404
from .models import InfoStudio,MonitorRegistrado
from .forms import MonitorRegistradoForm
from django.contrib import messages
from django.shortcuts import render
from usuarios.utils import login_requerido


@login_requerido
def registro_monitores(request):
    studio_id = request.session.get('usuario_id')
    print("studio_id:", studio_id)  # ← Esto ahora debe aparecer

    if not studio_id:
        messages.error(request, "Sesión expirada. Inicia sesión nuevamente.")
        return redirect('login')

    try:
        usuario = InfoStudio.objects.get(id=studio_id)
    except InfoStudio.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('login')

    # Validar cargo: solo admin puede acceder
    if usuario.cargo != 'admin':
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('inicio')  # o a una página de "no autorizado"

    # Si pasó la validación, procedemos con el código original usando studio_id del usuario
    studio_id = usuario.id_studio  # asumo que es así, revisa tu modelo

    
    monitores = MonitorRegistrado.objects.filter( estado=1, id_studio=studio_id,cargo="monitor")
    print("Monitores encontrados:", monitores.count())  # ✅ ahora modelos está definido

    if request.method == 'POST':
        accion = request.POST.get('accion')
        monitor_id = request.POST.get('monitor_id')

        if accion == 'guardar':

            form = MonitorRegistradoForm(request.POST, studio_id=studio_id)
            if form.is_valid():
                monitor = form.save(commit=False)
                monitor.studio_id = studio_id
                monitor.estado = 1
                monitor.id_studio = studio_id
                monitor.save()
                messages.success(request, "Monitor guardado correctamente.")
                return redirect('registro_monitores')


        
        elif accion == 'modificar':
            monitor = get_object_or_404(MonitorRegistrado, id=monitor_id, studio_id=studio_id)

            form = MonitorRegistradoForm(request.POST, instance=monitor, studio_id=studio_id)
            if form.is_valid():
                form.save()  # Solo guarda los campos del formulario
                messages.success(request, "Monitor modificado correctamente.")
                return redirect('registro_monitores')


        elif accion == 'eliminar':
            monitor = get_object_or_404(MonitorRegistrado, id=monitor_id, studio_id=studio_id)
            monitor.estado = 0
            monitor.save()
            messages.success(request, "Monitor eliminado correctamente.")
            return redirect('registro_monitores')
    else:
        form = MonitorRegistradoForm()

    return render(request, 'registro_monitores.html', {'form': form, 'monitores': monitores})
