from django import forms
from django.contrib.auth.models import User


class RegistroUsuarioForm(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150
    )
from .models import Servicio


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'categoria',
            'imagen_url',
            'disponible'
        ]

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')

        if precio is not None and precio <= 0:
            raise forms.ValidationError(
                "El precio debe ser mayor a 0."
            )

        return precio
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Este nombre de usuario ya existe."
            )

        return username

    def clean(self):
        datos = super().clean()

        password1 = datos.get('password1')
        password2 = datos.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Las contraseñas no coinciden."
            )

        return datos