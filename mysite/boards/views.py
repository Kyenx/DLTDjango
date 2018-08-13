from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponse
from .models import Board, Topic, Post, CustomUser
from .forms import NewTopicForm


def index(request): #home func
    
    boards = Board.objects.all() #return all objcs
    return render(request, 'index.html', {'boards': boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk) #Board.objects.get(pk=pk)
    return render(request, 'topics.html', {'board': board})

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
            topic.starter = user
            topic.save() #save

            post = Post.objects.create(  #Use regular objects.create method for models outs formAPI class
            message=form.cleaned_data.get('message'),
            topic=topic,
            created_by=user
            )

            return redirect('boards:board_topics', pk=board.pk)  # TODO: redirect to the created topic page, prevents double submitting

    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form':form}) #if fail - return view django form error generated messages 
