from django.shortcuts import reverse
from django.test import TestCase
from django.urls import resolve
from . import views

class SignUpViewTests(TestCase):
    
    def setUp(self):
        self.url = reverse("accounts:sign_up")
        self.response = self.client.get(self.url)

    def test_sign_up_view_success_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_sign_up_url_renders_sign_up_view(self):
        view = resolve('/auth/signup/')
        self.assertEquals(view.func, views.sign_up)



