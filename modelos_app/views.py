"""
from django.shortcuts import render, redirect, get_object_or_404
from .models import ModeloRegistrado
from .forms import ModeloRegistradoForm
from django.contrib import messages

def registro_modelos(request):
    studio_id = request.session.get('usuario_id')
    print("STUDIO_ID EN SESIÓN:", studio_id)
    if not studio_id:
        return redirect('login')

    form = ModeloRegistradoForm(studio_id=studio_id)

    if request.method == 'POST':
        accion = request.POST.get('accion')
        modelo_id = request.POST.get('modelo_id')

        if accion == 'guardar':
            form = ModeloRegistradoForm(request.POST, studio_id=studio_id)
            if form.is_valid():
                modelo = form.save(commit=False)
                modelo.studio_id = studio_id
                modelo.estado = True
                modelo.save()
                messages.success(request, "Modelo guardado correctamente.")
                return redirect('registro_modelos')

        elif accion in ['modificar', 'eliminar']:
            if not modelo_id:
                messages.error(request, "Debes seleccionar un modelo.")
                return redirect('registro_modelos')

            modelo = get_object_or_404(ModeloRegistrado, id=modelo_id, studio_id=studio_id)

            if accion == 'modificar':
                form = ModeloRegistradoForm(request.POST, instance=modelo, studio_id=studio_id)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Modelo modificado correctamente.")
                    return redirect('registro_modelos')

            elif accion == 'eliminar':
                modelo.estado = False
                modelo.save()
                messages.success(request, "Modelo eliminado correctamente.")
                return redirect('registro_modelos')

    #modelos = ModeloRegistrado.objects.filter(studio_id=studio_id, estado=True)
    

    print("studio_id:", studio_id)
    print("Modelos encontrados:", modelos.count())
    for m in modelos:
        print(m.nombre, m.studio_id, m.estado)
    modelos = ModeloRegistrado.objects.all()
    return render(request, 'registro_modelos.html', {'form': form, 'modelos': modelos})

    """

from django.shortcuts import render, redirect, get_object_or_404
from .models import ModeloRegistrado
from .forms import ModeloRegistradoForm
from django.contrib import messages
from django.shortcuts import render
from usuarios.utils import login_requerido


@login_requerido
def registro_modelos(request):
    studio_id = request.session.get('usuario_id')
    print("studio_id:", studio_id)  # ← Esto ahora debe aparecer

    if not studio_id:
        messages.error(request, "Sesión expirada. Inicia sesión nuevamente.")
        return redirect('login')

    
    modelos = ModeloRegistrado.objects.filter(studio_id=studio_id, estado=1)
    print("Modelos encontrados:", modelos.count())  # ✅ ahora modelos está definido
    print("studio_id en sesión:", studio_id)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        modelo_id = request.POST.get('modelo_id')

        if accion == 'guardar':
            #form = ModeloRegistradoForm(request.POST)
            form = ModeloRegistradoForm(request.POST, studio_id=studio_id)
            if form.is_valid():
                modelo = form.save(commit=False)
                modelo.studio_id = studio_id
                modelo.estado = 1
                modelo.save()
                messages.success(request, "Modelo guardado correctamente.")
                return redirect('registro_modelos')


        
        elif accion == 'modificar':
            modelo = get_object_or_404(ModeloRegistrado, id=modelo_id, studio_id=studio_id)

            form = ModeloRegistradoForm(request.POST, instance=modelo, studio_id=studio_id)
            if form.is_valid():
                form.save()  # Solo guarda los campos del formulario
                messages.success(request, "Modelo modificado correctamente.")
                return redirect('registro_modelos')


        elif accion == 'eliminar':
            modelo = get_object_or_404(ModeloRegistrado, id=modelo_id, studio_id=studio_id)
            modelo.estado = 0
            modelo.save()
            messages.success(request, "Modelo eliminado correctamente.")
            return redirect('registro_modelos')
    else:
        form = ModeloRegistradoForm()

    return render(request, 'registro_modelos.html', {'form': form, 'modelos': modelos})
