from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .models import MyUser
from .forms import UserSignUpForm
from .tokens import account_activation_token


class SignUp(CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('home')
    template_name = 'account/sign-up.html'

    def from_valid(self, form, commit=True):

        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])

        if commit:
            user.save()
            current_site = get_current_site(self.request)
            subject = 'Activate your account'
            message = render_to_string('account/account-activation-email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_str(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

        return super().from_valid(form)


def activate(request, uid, token):
    pass
