from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import MyUser
from .forms import UserSignUpForm


class SignUp(CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('home')
    template_name = 'account/sign-up.html'

    def from_valid(self, form, commit=True):

        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])

        if commit:
            user.save()
        return super().from_valid(form)
