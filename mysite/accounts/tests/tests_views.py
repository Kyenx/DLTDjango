from django.shortcuts import reverse
from django.test import TestCase
from django.urls import resolve
from .. import views
from ..forms import CustomUserCreationForm
from boards.models import CustomUser

class SignUpViewTests(TestCase):
    
    def setUp(self):
        self.url = reverse("sign_up")
        self.response = self.client.get(self.url)

    def test_sign_up_view_success_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_sign_up_url_renders_sign_up_view(self):
        view = resolve('/auth/signup/')
        self.assertEquals(view.func, views.sign_up)

    def test_sign_up_contains_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_sign_up_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
    
    def test_sign_up_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

    def test_form_has_fields(self):
        form = CustomUserCreationForm()
        expected = ['username', 'email', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

class SuccessSignUpTests(TestCase):

    def setUp(self):
        data = {
            'username':"johndoey",
            'email':"john@test.com",
            'password1':"qwertt1234",
            'password2':"qwertt1234"           
        }
        self.url = reverse("sign_up")
        self.response = self.client.post(self.url, data)
    
    def test_sign_up_valid_user_creation_to_redirection(self):
        self.assertTrue(CustomUser.objects.exists())
        self.assertRedirects(self.response, reverse('boards:index'))

    def test_user_authenticated(self):
        response = self.client.get(reverse("boards:index"))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSignUpTest(TestCase):

    def setUp(self):
        self.url = reverse("accounts:sign_up")
        self.response = self.client.post(self.url, {})

    def test_sign_up_invalid_post(self):
        #return form page - with errors
        self.assertEquals(self.response.status_code, 200)
    
    def test_sign_up_empty_entry(self):
        self.assertFalse(CustomUser.objects.exists())
    



