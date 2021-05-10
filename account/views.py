from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.models import User

from .forms import UserForm


class RegisterView(generic.CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = UserForm

    def form_valid(self, form):
        user = User.objects.create_user(
            form.cleaned_data.get('username'),
            form.cleaned_data.get('email'),
            form.cleaned_data.get('password')
        )
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.save()

        return redirect('login')


class AccountView(generic.DetailView):
    model = User
    template_name = 'account/details.html'
