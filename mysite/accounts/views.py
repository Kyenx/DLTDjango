from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from boards.models import CustomUser
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

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


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    fields = ('first_name', 'last_name', 'email')
    template_name = "my_account.html"
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user

