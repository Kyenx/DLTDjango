from django.test import TestCase
from django.urls import resolve, reverse

from .views import index, board_topics, new_topic

from .models import Board, Topic, Post

from .forms import NewTopicForm

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
        self.assertTemplateUsed(self.response, 'index.html')
    
    def test_index_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('boards:board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))



class BoardTopicsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')

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
    
    #first go to page, then test if page has link back
    def test_board_topics_contains_nav_links(self):
        board_topics_url = reverse('boards:board_topics', kwargs={'pk': self.board.pk})
        response = self.client.get(board_topics_url)
        home_url = reverse('boards:index')
        new_topic_url = reverse('boards:new_topic', kwargs={'pk': self.board.pk})

        self.assertContains(response, 'href="{0}"'.format(home_url)) #'href={0}'.format(home_url)
        self.assertContains(response, 'href="{0}"'.format(new_topic_url)) #new topic
        

class NewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('boards:new_topic', kwargs={'pk':self.board.pk})
        self.response = self.client.get(url)
    
    def test_new_topic_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_new_topic_view_not_found_status_code(self):
        url = reverse('boards:new_topic', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_new_topic_view_renders_correct_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_contains_link_back_to_board_topics(self):
        board_topics_url = reverse("boards:board_topics", kwargs={'pk':self.board.pk})
        self.assertContains(self.response, 'href="{0}'.format(board_topics_url))

    #Post Form tests
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    #More Form tests
    def test_contains_form(self):  # <- new test
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)
    


