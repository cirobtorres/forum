from collections import defaultdict

from django.core.exceptions import ValidationError

from .models import Session

class SessionValidator:
    def __init__(self, data: dict, errors: dict = None, errorClass: Exception = None, *args, **kwargs) -> None:
        self.errors = defaultdict(list) if errors is None else errors
        self.errorClass = ValidationError if errorClass is None else errorClass
        self.data = data
        self.clean()
    
    def clean(self, *args, **kwargs) -> None:
        self.clean_session_title()

        session_title = self.data.get('session_title', '')
        session_forum = self.data.get('session_forum')
        if Session.objects.filter(session_title=session_title, session_forum=session_forum).exists():
            self.errors['session_title'].append(ValidationError(message='Uma sessão de mesmo nome já existe.'))
        
        if self.errors:
            raise self.errorClass(self.errors)
    
    def clean_session_title(self, *args, **kwargs) -> str:
        session_title = self.data.get('session_title', '')
        if len(session_title) == 0:
            self.errors['session_title'].append(ValidationError(message='Sessões não podem ter título em branco.'))
        return session_title



class TopicValidator:

    def __init__(self, data: dict, errors: dict = None, errorClass: Exception = None, *args, **kwargs) -> None:
        self.errors = defaultdict(list) if errors is None else errors
        self.errorClass = ValidationError if errorClass is None else errorClass
        self.data = data
        self.clean()
    
    def clean(self, *args, **kwargs) -> None:
        self.clean_topic_title()
        self.clean_topic_content()

        if self.errors:
            raise self.errorClass(self.errors)
    
    def clean_topic_title(self, *args, **kwargs) -> str:
        topic_title = self.data.get('topic_title', '')
        if len(topic_title) == 0:
            self.errors['topic_title'].append(ValidationError(message='Dê um título ao seu tópico.'))
        return topic_title
    
    def clean_topic_content(self, *args, **kwargs) -> str:
        topic_content = self.data.get('topic_content', '')
        if len(topic_content) == 0:
            self.errors['topic_content'].append(ValidationError(message='O corpo do tópico não pode ser vazio.'))
        return topic_content