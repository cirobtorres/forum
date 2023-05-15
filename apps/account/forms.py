from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from .validators import UserValidator
from .models import Account, GENDER, STATE


class LoginForm(forms.Form):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Ex: johndoe'})

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class UpdateUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Ex: johndoe',})

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'username', 

    first_name = forms.CharField(label='Nome',error_messages={},help_text=None,)
    last_name = forms.CharField(label='Sobrenome',error_messages={},help_text=None,)
    username = forms.CharField(label='Usuário',error_messages={},
        help_text='Máximo de 30 caracteres. Exemplos: johndoe ou john_doe',
    )


class UpdateAccountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget.attrs.update({'placeholder': 'Ex: 06/09/2004',})

    class Meta:
        model = Account
        fields = 'birth_date', 'city', 'state', 'img', 
    
    field_order = 'birth_date', 'city', 'state', 'img', 
    
    birth_date = forms.DateField(label='Data de Nascimento', required=False, error_messages={}, help_text=None,)
    city = forms.CharField(label='Cidade', required=False, error_messages={}, help_text=None,)
    state = forms.ChoiceField(label='Estado', error_messages={}, help_text=None, choices=STATE,)
    img = forms.ImageField(label='', required=False, error_messages={}, help_text=None, widget=forms.FileInput(),)


class RegisterUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ex: John',})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Ex: Doe',})
        self.fields['username'].widget.attrs.update({'placeholder': 'Ex: jonhdoe',})
        self.fields['email'].widget.attrs.update({'placeholder': 'johndoe@email.com.br',})

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'username', 'email', 'password', 

    field_order = 'first_name', 'last_name', 'username', 'email', 'password', 
    fields_required = {'required': 'Campo obrigatório',}
    fields_invalid = {'invalid': 'Campo inválido',}
    fields_invalid_email = {'invalid': 'Entre um endereço de e-mail válido',}
    username_help_text = 'Máximo de 30 caracteres. Exemplos: johndoe ou john_doe'

    first_name = forms.CharField(
        label='Nome', error_messages={**fields_required, **fields_invalid}, help_text=None,)
    last_name = forms.CharField(
        label='Sobrenome', error_messages={**fields_required, **fields_invalid}, help_text=None, required=False,)
    username = forms.CharField(
        label='Usuário', error_messages={**fields_required, **fields_invalid}, help_text=username_help_text,)
    email = forms.CharField(
        label='E-mail', error_messages={**fields_required, **fields_invalid_email}, help_text=None,)
    password = forms.CharField(
        label='Senha', widget=forms.PasswordInput(), error_messages={**fields_required, **fields_invalid}, help_text=None,)
    password_confirmation = forms.CharField(
        label='Confirme a senha', widget=forms.PasswordInput(), error_messages={**fields_required, **fields_invalid}, help_text=None,)

    def clean(self, *args, **kwargs):
        UserValidator(self.cleaned_data, errorClass=ValidationError)
        return super().clean(*args, **kwargs)


class RegisterAccountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget.attrs.update({'placeholder': 'Ex: ' + now().strftime("%d/%m/%Y"),})
        self.fields['city'].widget.attrs.update({'placeholder': 'Ex: São Paulo',})
        self.fields['gender'].widget.attrs.update({'id': 'form-register-radio-input',})
        self.fields['state'].widget.attrs.update({'class': 'form-register-state',})
        self.fields['img'].widget.attrs.update({'class': 'form-register-img',})

    class Meta:
        model = Account
        fields = 'birth_date', 'gender', 'city', 'state', 'img', 
    
    field_order = 'gender', 'birth_date', 'city', 'state', 'img', 
    fields_invalid = {'invalid': 'Entre uma data válida'}
    input_formats = '%d-%m-%Y', '%d/%m/%Y',
    
    birth_date = forms.DateField(label='Data de nascimento', error_messages={**fields_invalid}, 
                                 help_text='', input_formats=input_formats, required=False,)
    gender = forms.ChoiceField(label='Sexo', error_messages={}, help_text='', choices=GENDER, 
                               widget=forms.RadioSelect(), initial='Masculino',)
    city = forms.CharField(label='Cidade', error_messages={}, help_text='', required=False,)
    state = forms.ChoiceField(label='UF', error_messages={}, help_text='', choices=STATE, initial='SP',)
    img = forms.ImageField(label='Imagem', error_messages={}, help_text='', required=False,)