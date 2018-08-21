from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponse
from  django.contrib.auth.decorators import login_required
from  django.db.models import Count
from .models import Board, Topic, Post, CustomUser
from .forms import NewTopicForm, PostForm


def index(request): #home func
    
    boards = Board.objects.all() #return all objcs
    return render(request, 'index.html', {'boards': boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk) #Board.objects.get(pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
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

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

def topic_reply(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('boards:topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'topic_reply.html', {"topic": topic, "form": form})
