from django import forms
from django.core.exceptions import ValidationError

from .models import Reply, Topic
from .validators import TopicValidator
from apps.tag.models import Tag


class ReplyForm(forms.ModelForm):
    
    class Meta:
        model = Reply
        fields = 'reply_content', 
    
    reply_content_errors = {
        'invalid': 'Comentário inválido', 
        'required': 'Preencha este campo'
        }
    
    reply_content = forms.CharField(label='', widget=forms.Textarea, error_messages={**reply_content_errors},)


class CreateTopicForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['tag'].widget.attrs.update({'class': 'topic-creation-tag-padding'})
        
    class Meta:
        model = Topic
        fields = 'topic_title', 'topic_content', 'fixed', 'tag', 
    
    topic_title = forms.CharField(label='Título', error_messages={}, help_text=None,)
    topic_content = forms.CharField(label='Texto', error_messages={}, help_text=None, widget=forms.Textarea,)
    fixed = forms.BooleanField(
        label='Fixar', help_text='Tópicos fixados aparecem na home ' \
            'do website e são sempre mantidos no topo da sessão', required=False,
        )
    tag = forms.ModelMultipleChoiceField(
        label='Tags', queryset=Tag.objects.all().order_by('name'), widget=forms.CheckboxSelectMultiple,
        )

    def clean(self, *args, **kwargs):
        TopicValidator(self.cleaned_data, errorClass=ValidationError)
        return super().clean(*args, **kwargs)