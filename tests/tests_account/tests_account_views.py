from ..test_base import (
        ObjectsFactoryMixins, 
        TestCase, 
        Account, User,
        Forum, Session, Topic, Reply, 
        Tag
    )


class AccountBaseTestViews(ObjectsFactoryMixins, TestCase):
    
    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()


class AccountViewsTest(AccountBaseTestViews):
    def test_account_view_register_access(self):
        ...
    
    def test_account_view_register_confirm(self):
        ...
    
    def test_account_view_login_access(self):
        ...
    
    def test_account_view_login_confirm(self):
        ...
    
    def test_account_view_logout_view(self):
        ...
    
    def test_account_view_dashboard(self):
        ...
    
    def test_account_view_update_confirm(self):
        ...
    
    def test_account_view_dashboard_view(self):
        ...
    
    def test_account_view_members_all(self):
        ...
    
    def test_account_view_members_staffs(self):
        ...
    
    def test_account_view_members_topics(self):
        ...
    
    def test_account_view_members_replies(self):
        ...
    
    def test_account_view_members_likes(self):
        ...