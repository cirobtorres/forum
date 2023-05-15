from django.urls import reverse

from ..test_base import (
        ObjectsFactoryMixins, 
        TestCase, 
        Account, User,
        Forum, Session, Topic, Reply, 
        Tag
    )


class AccountBaseTestUrl(ObjectsFactoryMixins, TestCase):
    
    def setUp(self) -> None:
        self.user:User = self.create_random_user()
        self.user.save()
        return super().setUp()
    
    
    def tearDown(self) -> None:
        return super().tearDown()


class AccountUrlsTest(AccountBaseTestUrl):
    def test_account_url_login_access(self):
        url_expected = '/login/'
        url_coded = reverse(viewname='account:login_access')
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_account_url_login_confirm(self):
        url_expected = '/login/confirm/'
        url_coded = reverse(viewname='account:login_confirm')
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_account_url_register_access(self):
        url_expected = '/register/'
        url_coded = reverse(viewname='account:register_access')
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_account_url_register_confirm(self):
        url_expected = '/register/confirm/'
        url_coded = reverse(viewname='account:register_confirm')
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_account_url_update_confirm(self):
        url_expected = f'/update/{self.user.username}/{self.user.id}/'
        url_coded = reverse(
            viewname='account:update_confirm', 
            kwargs={'name':self.user.username, 'id':self.user.id}
            )
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_account_url_logout_view(self):
        url_expected = '/logout/'
        url_coded = reverse(viewname='account:logout_view')
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_account_url_dashboard(self):
        url_expected = f'/dashboard/{self.user.username}/{self.user.id}/'
        url_coded = reverse(
            viewname='account:dashboard', 
            kwargs={'name':self.user.username, 'id':self.user.id, }
            )
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_account_url_dashboard_view(self):
        url_expected = f'/dashboard-view/{self.user.username}/{self.user.id}/'
        url_coded = reverse(
            viewname='account:dashboard_view', 
            kwargs={'name':self.user.username, 'id':self.user.id, }
            )
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_account_url_members_all(self):
        url_expected = '/members/'
        url_coded = reverse(viewname='account:members_all')
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_account_url_members_staffs(self):
        url_expected = '/members/staffs/'
        url_coded = reverse(viewname='account:members_staffs')
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_account_url_members_topics(self):
        url_expected = '/members/topics/'
        url_coded = reverse(viewname='account:members_topics')
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_account_url_members_replies(self):
        url_expected = '/members/replies/'
        url_coded = reverse(viewname='account:members_replies')
        self.assertEqual(first=url_expected, second=url_coded)
    
    def test_account_url_members_likes(self):
        url_expected = '/members/likes/'
        url_coded = reverse(viewname='account:members_likes')
        self.assertEqual(first=url_expected, second=url_coded)