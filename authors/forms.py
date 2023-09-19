from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def add_attr(field, attr_name, attr_new_val):
    field.widget.attrs[attr_name] = attr_new_val

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            'Password must have at least one uppercase and lowercase letter, '
            'one number and the len must be at least 8 characaters', 
            code='invalid'
            )

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['username'], 'placeholder', 'report your username')
        add_attr(self.fields['first_name'], 'placeholder', 'Write your first name here')
        add_attr(self.fields['last_name'], 'placeholder', 'Write your last name here')
        add_attr(self.fields['email'], 'placeholder', 'Report your email')
        add_attr(self.fields['password'], 'placeholder', 'Type your password')
        add_attr(self.fields['password2'], 'placeholder', 'Confirm your password')

    first_name = forms.CharField(
        error_messages={
            'required': 'first name must not be empty',
        },
        label='Primeiro nome',
    )
    last_name = forms.CharField(
        error_messages={
            'required': 'last name must not be empty',
        },
        label='Último nome',
    )
    username = forms.CharField(
        error_messages={
            'required': 'Esse campo é obrigatorio seu arrombado',
            'max_length': 'You exceeded the limit of 150 characters',
            'min_length': 'You have not reached the min len of 4 characters',
        },
        label='Digite seu usuario',
        help_text='Your username here',
        min_length=4,
        max_length=150,
    )
    email = forms.EmailField(
        error_messages={
            'required': 'Email must not be empty',
        },
        label='Endereço de email',
        help_text='email must be valid',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password here'
        }),
        label='Password1',
        validators=[strong_password],
        error_messages={
            'required': 'Password must not be empty',
        },

    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password here'
        }),
        label='Password2',
        help_text='both passwords must be equal',
        error_messages={
            'required': 'Please, repeat your password',
        },
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password'] 


    # def clean_password(self):
    #     data = self.cleaned_data.get('password')

    #     if 'atencao' in data:
    #         self.add_error(
    #             'password',
    #             ValidationError(
    #             'Palavra %(pipoca)s detectada',
    #             code='invalid',
    #             params={
    #                 'pipoca': '"ATENÇÃO"',
    #             }
    #             )
    #         )

    #     return data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(
                    'This email is already in use, use another',
                    code='invalid'
                )
        return email

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
    
