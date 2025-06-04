from django import forms
from .models import MonitorRegistrado
from django.contrib.auth.hashers import make_password

class MonitorRegistradoForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        password = self.cleaned_data['password']
        return make_password(password)
    
    def __init__(self, *args, studio_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.studio_id = studio_id
        if self.instance and self.instance.pk:
            self.fields.pop('username', None)

    

    def clean_username(self):
        if 'username' in self.cleaned_data:  # solo si está en el form
            username = self.cleaned_data['username']
            qs = MonitorRegistrado.objects.filter(
                username=username,
                id_studio=self.studio_id,
                cargo = "monitor",
                estado=1
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Este usuario ya está registrado en este estudio.")
            return username

    class Meta:
        model = MonitorRegistrado
        fields = ['name', 'username', 'password']
