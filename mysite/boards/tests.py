from django.test import TestCase
from django.urls import resolve, reverse

from .views import index

class IndexViewTests(TestCase):
    def test_index_view_status_code(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_index_url_resolves_index_view(self):
        view = resolve('/')
        self.assertEquals(view.func, index)

    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'boards/index.html')
