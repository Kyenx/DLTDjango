from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponse
from  django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from  django.db.models import Count
from .models import Board, Topic, Post, CustomUser
from .forms import NewTopicForm, PostForm

from django.views.generic import UpdateView, ListView
from django.utils import timezone



class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = "index.html"

''' Old function based method
def index(request): #home func

    boards = Board.objects.all() #return all objcs
    return render(request, 'index.html', {'boards': boards})
'''
def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk) #Board.objects.get(pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 20)
    
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        #Go back to first page
        topics = paginator.page(1)
    except EmptyPage:
        #Attempt thru url, go to max/last page
        topics = paginator.page(paginator.num_pages)


    return render(request, 'topics.html', {'board': board, "topics":  topics})

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST': #check req type

        user = CustomUser.objects.first()  # TODO: get the currently logged in user

        '''
        Old method - without FormAPI

        subject = request.POST['subject']
        message = request.POST['message']

        topic = Topic.objects.create(
            subject=subject,
            board=board,
            starter=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )
        '''
        form = NewTopicForm(request.POST) #make form from POST
        if form.is_valid(): #check validity 
            topic = form.save(commit=False) #false commit = doesnt save until save called again
            topic.board = board
            topic.starter = request.user
            topic.save() #save

            post = Post.objects.create(  #Use regular objects.create method for models outs formAPI class
            message=form.cleaned_data.get('message'),
            topic=topic,
            created_by=request.user
            )

            return redirect('boards:topic_posts', pk=pk, topic_pk=topic.pk)  # TODO: redirect to the created topic page, prevents double submitting

    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form':form}) #if fail - return view django form error generated messages 

''' Oldie without GCBV
def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})
'''

class PostListView(ListView):
    model = Post
    template_name = "topic_posts.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_context_data(self, **kwargs):

        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
            
        kwargs['topic'] = self.topic
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self):
        #queryset = super().get_queryset()
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))#self.topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
        queryset = self.topic.posts.order_by('created_at')
        return queryset
    

@login_required
def topic_reply(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()
            
            return redirect('boards:topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'topic_reply.html', {"topic": topic, "form": form})



@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView): #Using UpdateView GCBV
    model = Post
    fields = ('message', ) #Usually and better to provide own form class -> form_class = PostForm
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk' #What we pass in Urls.py in path field
    context_object_name = 'post' #If not assigned, default returned object = object!!!

    def get_queryset(self): #override default to provide more targeted database
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):   #form_valid is default methods - overwritten to set some extra fields [update_by, updated_at]
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('boards:topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)