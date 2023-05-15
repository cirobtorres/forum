from selenium.webdriver.common.by import By
from time import sleep

from django.urls import reverse
from django.test import LiveServerTestCase  # css OFF
from django.contrib.staticfiles.testing import StaticLiveServerTestCase  # css ON

from ...test_base import ObjectsFactoryMixins, TestCase, Forum, Session, User
from utils.browser import set_up_chrome_webdriver

class ForumBaseTestForms(ObjectsFactoryMixins, StaticLiveServerTestCase, TestCase):
    
    def setUp(self) -> None:
        self.browser = set_up_chrome_webdriver()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()


class ForumFormsTest(ForumBaseTestForms):

    def test_form_create_topic_tag_field_css_class(self):
        ...