from string import printable
from random import SystemRandom

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.db.models import Subquery, OuterRef

from ..tag.models import Tag


class Forum(models.Model):
    forum_user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True,)
    forum_title = models.CharField(max_length=65,)
    forum_description = models.CharField(max_length=65, default='', null=True, blank=True,)
    forum_slug = models.SlugField(unique=True, null=True,)
    forum_timestamp_create = models.DateTimeField(auto_now_add=True,)
    forum_timestamp_update = models.DateTimeField(auto_now=True,)

    def __str__(self) -> str:
        return self.forum_title

    class Meta:
        verbose_name_plural = 'Foruns'


class Session(models.Model):
    session_forum = models.ForeignKey(to=Forum, on_delete=models.CASCADE, null=True,)
    session_user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True,)
    session_title = models.CharField(max_length=65,)
    session_description = models.CharField(max_length=65, default='', null=True, blank=True,)
    session_slug = models.SlugField(unique=True, null=True,)
    session_timestamp_create = models.DateTimeField(auto_now_add=True,)
    session_timestamp_update = models.DateTimeField(auto_now=True,)
    staff_only = models.BooleanField(blank=True, default=False, help_text="Only staffs are allowed to create topics in this 'Session'",)

    def __str__(self) -> str:
        return self.session_title
    
    class Meta:
        verbose_name_plural = 'Sessions'


class Topic(models.Model):
    topic_user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True,)
    topic_session = models.ForeignKey(to=Session, on_delete=models.CASCADE, null=True,)
    topic_title = models.CharField(max_length=65,)
    topic_content = models.TextField()
    topic_slug = models.SlugField(unique=True, null=True, max_length=65,)
    topic_timestamp_create = models.DateTimeField(auto_now_add=True,)
    topic_timestamp_update = models.DateTimeField(auto_now=True,)
    views = models.IntegerField(default=0,)
    fixed = models.BooleanField(default=False, help_text="Showcase on home-page",)
    block = models.BooleanField(blank=True, default=False, help_text="Only moderators are allowed to post",)
    likes = models.ManyToManyField(to=User, related_name='topic_likes', blank=True,)
    tag = models.ManyToManyField(to=Tag,)

    def __str__(self) -> str:
        return self.topic_title
    
    def total_likes(self) -> int:
        return self.likes.count()
    
    def save(self, *args, **kwargs):
        random_code = ''.join(SystemRandom().choices(population=printable, k=20))
        if not self.topic_slug:
            while True:
                new_slug = slugify(value=f'{self.topic_session}-{self.topic_title}-{random_code}')
                try:
                    topic_exists = Topic.objects.get(topic_slug=new_slug)
                except Topic.DoesNotExist:
                    topic_exists = None
                if not topic_exists:
                    break
            self.topic_slug = new_slug
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Topics'


class ReplyManager(models.Manager):
    def subquery(self, *fields:str, **kwargs,):
        ordering: str = kwargs.get('ordering', '-reply_timestamp_create')
        return Subquery(Reply.objects.\
                        filter(reply_topic_id=OuterRef('id')) \
                            .order_by(ordering) \
                                .values(*fields))


class Reply(models.Model):
    objects = ReplyManager()

    reply_user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True,)  # default = 1
    reply_topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE, default='', null=True,)
    reply_content = models.TextField()
    reply_timestamp_create = models.DateTimeField(auto_now_add=True,)
    reply_timestamp_update = models.DateTimeField(auto_now=True,)
    likes = models.ManyToManyField(to=User, related_name='reply_likes', blank=True,)

    def __str__(self) -> str:
        return str(self.reply_topic)
    
    def total_likes(self) -> int:
        return self.likes.count()
    
    class Meta:
        ordering = 'reply_timestamp_create', 
        verbose_name_plural = 'Replies'