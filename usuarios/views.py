from django.shortcuts import render, redirect
from django.contrib import messages
from .models import InfoStudio
from .utils import login_requerido
from django.contrib.auth.hashers import check_password

def login_usuario(request):
    

    if request.method == 'POST':
        username = request.POST['username']
        password_ingresada = request.POST['password']

        try:
            usuario = InfoStudio.objects.get(username=username)
            hash_guardado = usuario.password  # ya es un string compatible con check_password

            #if check_password(password_ingresada, hash_guardado):
            #    request.session['usuario_id'] = usuario.id
            #    return redirect('inicio')
            if check_password(password_ingresada, hash_guardado):
                request.session['usuario_id'] = usuario.id
                request.session['id_studio'] = usuario.id_studio
                request.session['cargo'] = usuario.cargo
                request.session['name'] = usuario.name
                return redirect('inicio')
            else:
                messages.error(request, 'Contraseña incorrecta')

        except InfoStudio.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'login.html')


@login_requerido
def inicio(request):
    
    usuario_id = request.session.get('usuario_id')
    id_studio = request.session.get('id_studio')
    name = request.session.get('name')
    usuario = InfoStudio.objects.get(id=usuario_id)
    return render(request, 'inicio.html', {'usuario': usuario, 'usuario_id':usuario_id,'id_studio':id_studio,'name':name})

def logout_usuario(request):
    
    request.session.flush()  # Elimina todos los datos de sesión
    return redirect('login')

#def registro_modelos(request):
#    return render(request, 'registro_modelos.html')

#def tabla_posiciones(request):
#    return render(request, 'tabla_posiciones.html')

#def ver_promedios(request):
#    return render(request, 'ver_promedios.html')

def home(request):
    return render(request, 'login.html')