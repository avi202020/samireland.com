from seleniumx import TestCaseX
from django.test import TestCase
import samireland.views as views

class UrlTests(TestCase, TestCaseX):

    def test_home_url(self):
        self.check_url_returns_view("/", views.home)


    def test_login_url(self):
        self.check_url_returns_view("/authenticate/", views.login)


    def test_logout_url(self):
        self.check_url_returns_view("/logout/", views.logout)