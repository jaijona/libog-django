from django.shortcuts import redirect

def login_requerido(view_func):
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            return redirect('login')  # Si no ha iniciado sesión, lo redirige
        return view_func(request, *args, **kwargs)
    return wrapper
