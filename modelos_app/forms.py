from django import forms
from .models import ModeloRegistrado
"""
class ModeloRegistradoForm(forms.ModelForm):
    def __init__(self, *args, studio_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.studio_id = studio_id

        # Si estamos editando un modelo existente, removemos el campo "usuario"
        if self.instance and self.instance.pk:
            self.fields.pop('usuario', None)

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        qs = ModeloRegistrado.objects.filter(
            nombre=nombre,
            studio_id=self.studio_id,
            estado=1
        )

        # Si estamos editando (modificar), ignorar el actual
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Ya existe un modelo con este nombre en este estudio.")
        return nombre
    
    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']
        qs = ModeloRegistrado.objects.filter(
            usuario=usuario,
            studio_id=self.studio_id,
            estado=1  # o True, dependiendo de cómo tratas el campo
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Este usuario ya está registrado en este estudio.")
    
        return usuario


    class Meta:
        model = ModeloRegistrado
        fields = ['nombre', 'usuario', 'jornada', 'genero']

"""
class ModeloRegistradoForm(forms.ModelForm):
    def __init__(self, *args, studio_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.studio_id = studio_id
        if self.instance and self.instance.pk:
            self.fields.pop('usuario', None)

    

    def clean_usuario(self):
        if 'usuario' in self.cleaned_data:  # solo si está en el form
            usuario = self.cleaned_data['usuario']
            qs = ModeloRegistrado.objects.filter(
                usuario=usuario,
                studio_id=self.studio_id,
                estado=1
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Este usuario ya está registrado en este estudio.")
            return usuario

    class Meta:
        model = ModeloRegistrado
        fields = ['nombre', 'usuario', 'jornada', 'genero']
