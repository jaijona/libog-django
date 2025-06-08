from django import forms
from .models import IngresoTokens
from modelos_app.models import ModeloRegistrado

class IngresoTokensForm(forms.ModelForm):
    class Meta:
        model = IngresoTokens
        fields = ['id_modelo', 'fecha', 'token_cb', 'token_otro']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        studio_id = kwargs.pop('studio_id', None)
        super().__init__(*args, **kwargs)
        if studio_id:
            self.fields['id_modelo'].queryset = ModeloRegistrado.objects.filter(studio_id=studio_id, estado=1)
