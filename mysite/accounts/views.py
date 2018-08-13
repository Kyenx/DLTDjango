from django.shortcuts import render, get_object_or_404

def sign_up(request):
    return render(request, 'sign_up.html')
