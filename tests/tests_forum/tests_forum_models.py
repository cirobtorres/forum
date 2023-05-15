from ..test_base import ObjectsFactoryMixins, TestCase, User, Forum, Session, Topic, Reply


class ForumBaseTestModels(ObjectsFactoryMixins, TestCase):
    
    def setUp(self) -> None:
        self.user:User = self.create_random_user()
        self.user.save()
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()


class ForumModelsTest(ForumBaseTestModels):
    
    # Forum -------------------------------------------------------------------
    def test_models_forum_str_dunder_name(self):
        forum:Forum = self.create_random_forum(topic_title='This is my Forum Title')
        self.assertEqual(first=forum.forum_title, second=str(forum))
    
    # Session -----------------------------------------------------------------
    def test_models_forum_session_str_dunder_name(self):
        session:Session = self.create_random_session(topic_title='This is my Session Title')
        self.assertEqual(first=session.session_title, second=str(session))

   # Topic --------------------------------------------------------------------
    def test_models_forum_topic_str_dunder_name(self):
        topic:Topic = self.create_random_topic(topic_title='This is my Topic Title')
        self.assertEqual(first=topic.topic_title, second=str(topic))
    
    def test_models_forum_topic_slug_generation(self):
        topic:Topic = self.create_random_topic(topic_title="I'm the base to create this slug")
        self.assertTrue(expr='im-the-base-to-create-this-slug' in topic.topic_slug)
    
    def test_models_forum_topic_slug_generation_exists(self):
        # Pratically impossible to achiev
        ...
    
    def test_models_forum_topic_likes_count(self):
        topic:Topic = self.create_random_topic()
        topic.likes.add(self.user)
        self.assertTrue(expr=topic.total_likes() == 1)
    
    def test_models_forum_topic_max_length(self):
        ...
    
    # Reply -------------------------------------------------------------------
    def test_models_forum_reply_str_dunder_name(self):
        topic:Topic = self.create_random_topic(topic_title='This is the Title Needed to Pass my Test')
        reply:Session = self.create_random_reply(reply_topic=topic)
        self.assertEqual(first='This is the Title Needed to Pass my Test', second=str(reply))
    
    def test_models_forum_reply_likes_count(self):
        reply:Reply = self.create_random_reply()
        reply.likes.add(self.user)
        self.assertTrue(expr=reply.total_likes() == 1)
    
    def test_models_forum_reply_manager_subquery(self):
        ...