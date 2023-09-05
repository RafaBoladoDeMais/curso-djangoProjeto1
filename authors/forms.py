from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    field.widget.attrs[attr_name] = attr_new_val

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['username'], 'placeholder', 'informe seu usuario')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password here'
        }),
        label='Password1',

    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password here'
        }),
        label='Password2',
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password'] 
        labels = {
            'username': 'Digite seu usuario',
        }
        help_texts = {
            'email': 'O email tem que ser valido',
        }
        error_messages = {
            'username': {
                'required': 'Esse campo é obrigatorio seu arrombado',
                'max-length': 'Voce ultrapassou o limite da caracteres',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Escreva seu username aqui',
            }),
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atencao' in data:
            self.add_error(
                'password',
                ValidationError(
                'Palavra %(pipoca)s detectada',
                code='invalid',
                params={
                    'pipoca': '"ATENÇÃO"',
                }
                )
            )

        return data
    
    def clean(self):
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('password2')

        if pass2 != pass1:
            raise ValidationError({
                'password':ValidationError(
                'both passwords must be %(value)s',
                code='invalid',
                params={
                    'value': '"EQUAL"',
                }
                ),
                'password2': 'both passwords must be "EQUAL"', 
                }
                )
        return super().clean()
    
