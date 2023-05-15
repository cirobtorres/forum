from random import randint

from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase

from apps.account.models import Account
from apps.forum.models import Forum, Session, Topic, Reply
from apps.tag.models import Tag

from utils.faker import DotAccessFaker, fake


class ObjectsFactoryMixins(DotAccessFaker):

    @staticmethod
    def get_create_time():
        return timezone.now()


    @staticmethod
    def create_tag(tag_name:str=None, **kwargs) -> Tag:
        size = kwargs.get('size', randint(1, 4))
        if tag_name is None:
            tag_name = fake.sentence(nb_words=size)
        return Tag.objects.create(name=tag_name)


    def create_user(
            self, 
            first_name:str='Nome', 
            last_name:str='Sobrenome', 
            username:str='usuario',
            email:str='usuario@email.com',
            password:str='1',
            account:dict=None,
        ) -> User:

        user:User = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            )
        
        Account(user=user, **account)

        return user


    def create_forum(
            self, 
            forum_user:User=None, 
            forum_title:str='Forum Title',
            forum_description:str='Forum Description',
            forum_slug:str=None
        ) -> Forum:
        
        if forum_slug is None:
            forum_slug = DotAccessFaker.randomized_slug(slug_from=forum_title)
        
        return Forum.objects.create(
            forum_user=forum_user,
            forum_title=forum_title,
            forum_description=forum_description,
            forum_slug=forum_slug,
            forum_timestamp_create=self.get_create_time(),
            forum_timestamp_update=self.get_create_time(),
        )


    def create_session(
            self, 
            session_forum:Forum=None, 
            session_user:User=None, 
            session_title:str='Session Title', 
            session_description:str='Session Description',
            session_slug:str=None,
            staff_only:bool=False,
        ) -> Session:

        session_slug = session_slug if session_slug is not None \
            else DotAccessFaker.randomized_slug(slug_from=session_title)

        return Session.objects.create(
            session_forum=session_forum,
            session_user=session_user,
            session_title=session_title,
            session_description=session_description,
            session_slug=session_slug,
            session_timestamp_create=self.get_create_time(),
            session_timestamp_update=self.get_create_time(),
            staff_only=staff_only,
        )
    

    def create_topic(
            self,
            topic_user:User=None,
            topic_session:Session=None,
            topic_title:str='Topic Title',
            topic_content:str='Topic Content',
            topic_slug:str=None,
            fixed:bool=False,
            block:bool=False,
            likes:'tuple[User]'=None,
            tag:'tuple[Tag]'=None,
        ) -> Topic:

        topic_user:User = topic_user if topic_user is not None else {}
        topic_session:Session = topic_session if topic_session is not None else {}
        
        topic:Topic = Topic.objects.create(
            topic_user=self.create_user({**topic_user}),
            topic_session=self.create_user({**topic_session}),
            topic_title=topic_title,
            topic_content=topic_content,
            topic_slug=topic_slug,
            topic_timestamp_create=self.get_create_time(),
            topic_timestamp_update=self.get_create_time(),
            fixed=fixed,
            block=block,
            )
        
        if tag:
            topic.tag.set(*tag)
        if likes:
            topic.likes.set(*likes)
        
        return topic
    

    def create_reply(
            self,
            reply_user:User=None,
            reply_topic:Topic=None,
            reply_content:str='Reply Content',
            likes:'tuple[User]'=None,
        ) -> Reply:

        reply_user:User = reply_user if reply_user is not None else {}
        reply_topic:Topic = reply_topic if reply_topic is not None else {}

        reply = Reply.objects.create(
            reply_user=self.create_user({**reply_user}),
            reply_topic=self.create_topic({**reply_topic}),
            reply_content=reply_content,
            reply_timestamp_create=self.get_create_time(),
            reply_timestamp_update=self.get_create_time(),
        )

        if likes:
            reply.likes.set(*likes)
        
        return reply
    

    def create_random_user(self, **kwargs) -> User:
        return self.create_user(**self.randomized_user(**kwargs))
    

    def create_random_forum(self, forum_user:User=None, **kwargs) -> Forum:
        forum:Forum = self.create_forum(
                forum_user=forum_user, 
                **self.randomized_forum(**kwargs),
            )
        return forum


    def create_random_session(
                self, 
                session_user:User=None, 
                session_forum:Forum=None, 
                **kwargs
            ) -> Session:
        
        session:Session = self.create_session(
                session_user=session_user, 
                session_forum=session_forum, 
                **self.randomized_session(**kwargs),
            )

        return session
    

    def create_random_topic(
                self, 
                topic_user:User=None, 
                topic_session:Session=None, 
                tag:tuple[Tag]=None, 
                **kwargs
            ) -> Topic:

        topic:Topic = Topic.objects.create(
            topic_user=topic_user, 
            topic_session=topic_session, 
            **self.randomized_topic(**kwargs),
            )

        if tag:
            topic.tag.set(tag)

        return topic
    

    def create_random_reply(
                self, 
                reply_user:User=None, 
                reply_topic:Topic=None, 
                **kwargs
            ) -> Reply:
        
        reply:Reply = Reply.objects.create(
                reply_user=reply_user,
                reply_topic=reply_topic,
                **self.randomized_reply(**kwargs),
            )

        return reply


    def create_random_tag(self, size:int=1, **kwargs) -> tuple[Tag]:
        if size == 1:
            return self.create_tag(**kwargs)
        else:
            return [self.create_tag(**kwargs) for iter in range(0, size)]