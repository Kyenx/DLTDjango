from django.test import TestCase
from django.urls import resolve, reverse

from .views import index, board_topics

from .models import Board

class IndexViewTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('boards:index')
        self.response = self.client.get(url)

    def test_index_view_status_code(self):
        #url = reverse('boards:index')
        #response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)
    
    def test_index_url_resolves_index_view(self):
        view = resolve('/')
        self.assertEquals(view.func, index)

    def test_index_view_uses_correct_template(self):
        #response = self.client.get(reverse('boards:index'))
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'boards/index.html')
    
    def test_index_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('boards:board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))



class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('boards:board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('boards:board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)
