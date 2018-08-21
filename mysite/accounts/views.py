from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404, redirect

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('boards:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'sign_up.html', {'form': form})
