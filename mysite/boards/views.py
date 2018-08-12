from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from .models import Board


def index(request):
    
    boards = Board.objects.all()
    return render(request, 'boards/index.html', {'boards': boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)#Board.objects.get(pk=pk)
    return render(request, 'boards/topics.html', {'board': board})
