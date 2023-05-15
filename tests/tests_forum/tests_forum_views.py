from ..test_base import ObjectsFactoryMixins, TestCase


class ForumBaseTestViews(ObjectsFactoryMixins, TestCase):
    
    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()


class ForumViewsTest(ForumBaseTestViews):
    
    def test_forum_view_home(self):
        ...
    
    def test_forum_view_session(self):
        ...
    
    def test_forum_view_topic(self):
        ...