from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from collections import defaultdict
from re import search, fullmatch


class UserValidator:
    
    def __init__(self, data: dict, errors: dict = None, errorClass: Exception = None, *args, **kwargs) -> None:
        self.errors = defaultdict(list) if errors is None else errors
        self.errorClass = ValidationError if errorClass is None else errorClass
        self.data = data
        self.clean()
    
    def clean(self, *args, **kwargs):

        self.clean_first_name()
        self.clean_username()
        self.clean_email()
        self.clean_password()
        
        password = self.data.get('password', '')
        password_confirmation = self.data.get('password_confirmation', '')
        
        if password != password_confirmation:
            pass_error_msg = ValidationError(message='As senhas não conferem', code='invalid')
            self.errors['password'].append(pass_error_msg)
            self.errors['password_confirmation'].append(pass_error_msg)

        if self.errors:
            raise self.errorClass(self.errors)
    
    def clean_first_name(self, *args, **kwargs) -> str:
        first_name = self.data.get('first_name', '')
        if len(first_name) < 4:
            self.errors['first_name'].append('Nome não pode ter menos que quatro caracteres')
        return first_name

    def clean_username(self, *args, **kwargs) -> str:
        username = self.data.get('username', '')
        if User.objects.filter(username=username).exists():
            self.errors['username'].append(ValidationError(message='Este usuário já esá em uso'))
        if search(pattern=r'\W', string=username):
            self.errors['username'].append(ValidationError(message='Usuário não pode ter caracteres especiais ou espaços em branco'))
        if search(pattern=r'\d', string=username):
            self.errors['username'].append(ValidationError(message='Usuário não pode ter dígitos'))
        if len(username) < 4 or len(username) > 30:
            self.errors['username'].append(ValidationError(message='Usuário não pode ter menos de quatro ou mais de trinta caracteres'))
        return username.lower()

    def clean_email(self, *args, **kwargs) -> str:
        email = self.data.get('email', '').lower()
        if not fullmatch(pattern=r'^(?!\.\.*)([a-zA-Z0-9._]{1,64}@)([a-zA-Z]{1,64}\.)(com|gov|edu|org)(\.br)?|(net)?$', string=email):
            self.errors['email'].append('Esse formato de e-mail não é permitido')
        if User.objects.filter(email=email).exists():
            self.errors['email'].append('Este e-mail já está em uso')
        return email
    
    def clean_password(self, *args, **kwargs) -> str:
        password = self.data.get('password', '')

        if search(pattern=r'\s', string=password):
            self.errors['password'].append(ValidationError(message='A senha não deve conter espaços',))
        if not search(pattern=r'(?=.{8,12}$)', string=password):
            self.errors['password'].append(ValidationError(message='A senha deve conter entre 8 e 12 caracteres'))
        if not search(pattern=r'(?=.*[A-Z])', string=password):
            self.errors['password'].append(ValidationError(message='A senha deve conter ao menos um caractere maiúsculo'))
        if not search(pattern=r'(?=.*[a-z])', string=password):
            self.errors['password'].append(ValidationError(message='A senha deve conter ao menos um caractere minúsculo'))
        if not search(pattern=r'(?=.*[0-9])', string=password):
            self.errors['password'].append(ValidationError(message='A senha deve conter ao menos um caractere numérico'))
        if not search(pattern=r'(?=.*[!@#$%&^~,.+-])', string=password):
            self.errors['password'].append(ValidationError(message='A senha deve conter ao menos um caractere especial'))
        
        return password