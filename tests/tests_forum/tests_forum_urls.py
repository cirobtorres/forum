from django.urls import reverse

from ..test_base import (
        ObjectsFactoryMixins, 
        TestCase, 
        Account, User,
        Forum, Session, Topic, Reply, 
        Tag
    )


class ForumBaseTestUrls(ObjectsFactoryMixins, TestCase):
    
    def setUp(self) -> None:
        self.user:User = self.create_random_user()
        self.user.save()
        self.session:Session = self.create_random_session(session_user=self.user)
        self.topic:Topic = self.create_random_topic(
            topic_user=self.user, topic_session=self.session
            )
        self.reply:Reply = self.create_random_reply(
            reply_user=self.user, reply_topic=self.topic
            )
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()


class ForumUrlsTest(ForumBaseTestUrls):
    def test_url_forum_home(self):
        url_expected = '/'
        url_coded = reverse(viewname='forum:home')
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_url_forum_session(self):
        url_expected = f'/session/1/'  # /session/<int:session_id>/
        url_coded = reverse(
            viewname='forum:session', 
            kwargs={
                'session_id': self.session.id,
                },
            )
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_url_forum_topic(self):
        url_expected = f'/session/1/topic/1/'  # /session/<int:session_id>/topic/<int:topic_id/
        url_coded = reverse(
            viewname='forum:topic', 
            kwargs={
                'session_id': self.topic.topic_session_id, 
                'topic_id': self.topic.id,
                },
            )
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_url_forum_reply(self):
        url_expected = f'/reply-to/1/topic/1/'  # reply-to/<int:session_id>/topic/<int:topic_id>/
        url_coded = reverse(
            viewname='forum:reply',
            kwargs={
                'session_id': self.reply.reply_topic.topic_session_id,
                'topic_id': self.reply.reply_topic_id,
                },
        )
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_url_forum_topic_creation(self):
        url_expected = f'/topic-creation/1/'  # /topic-creation/<int:session_id>/
        url_coded = reverse(
            viewname='forum:topic_creation', 
            kwargs={
                'session_id': self.topic.topic_session_id,
                },
            )
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_url_forum_topic_confirm(self):
        url_expected = f'/topic-create/1/'  # /topic-create/<int:session_id>/
        url_coded = reverse(
            viewname='forum:topic_confirm', 
            kwargs={
                'session_id': self.topic.topic_session_id,
                },
            )
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_url_forum_topic_delete(self):
        url_expected = f'/delete-topic/1/topic/1/'  # /delete-topic/<int:session_id>/topic/<int:topic_id>/
        url_coded = reverse(
            viewname='forum:topic_delete', 
            kwargs={
                'session_id': self.topic.topic_session_id,
                'topic_id': self.topic.id,
                },
            )
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_url_forum_reply_delete(self):
        url_expected = f'/delete-reply/1/topic/1/1/'  # /delete-reply/<int:session_id>/topic/<int:topic_id>/<int:reply_id>/
        url_coded = reverse(
            viewname='forum:reply_delete', 
            kwargs={
                'session_id': self.reply.reply_topic.topic_session_id,
                'topic_id': self.reply.reply_topic_id,
                'reply_id': self.reply.id,
                },
            )
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_url_forum_tag(self):
        tag:Tag = self.create_random_tag(tag_name='This is my Tag')
        url_expected = f'/search-tag/This%20is%20my%20Tag/1/'  # /search-tag/<str:tag_name>/<int:tag_id>/
        url_coded = reverse(
            viewname='forum:tag', 
            kwargs={
                'tag_name': tag.name,
                'tag_id': tag.id,
                },
            )
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_url_forum_query(self):
        url_expected = f'/search/'
        url_coded = reverse(viewname='forum:query')
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_url_forum_like_topic(self):
        url_expected = f'/like/1/1/'  # /like/<int:session_id>/<int:topic_id>/
        url_coded = reverse(
            viewname='forum:like_topic', 
            kwargs={
                'session_id': self.topic.topic_session_id,
                'topic_id': self.topic.id,
                },
            )
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_url_forum_like_reply(self):
        url_expected = f'/like/1/1/1/'  # /like/<int:session_id>/<int:topic_id>/<int:reply_id>/
        url_coded = reverse(
            viewname='forum:like_reply', 
            kwargs={
                'session_id': self.topic.topic_session_id,
                'topic_id': self.topic.id,
                'reply_id': self.reply.id,
                },
            )
        self.assertEqual(first=url_expected, second=url_coded)