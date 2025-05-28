from django.shortcuts import render, redirect
from django.contrib import messages
from .models import InfoStudio
import bcrypt
from .utils import login_requerido

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password_ingresada = request.POST['password'].encode('utf-8')

        try:
            usuario = InfoStudio.objects.get(username=username)
            hash_guardado = usuario.password.encode('utf-8')

            if bcrypt.checkpw(password_ingresada, hash_guardado):
                request.session['usuario_id'] = usuario.id
                return redirect('inicio')
            else:
                messages.error(request, 'Contraseña incorrecta')

        except InfoStudio.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'login.html')

@login_requerido
def inicio(request):
    usuario_id = request.session.get('usuario_id')
    return render(request, 'inicio.html', {'usuario_id': usuario_id})

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