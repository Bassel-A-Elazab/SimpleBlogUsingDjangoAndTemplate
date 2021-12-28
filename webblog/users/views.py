from django.views.generic import CreateView
from django.contrib.auth import login
from django.shortcuts import render, redirect
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
    template_name = 'account/signup.html'

    def form_valid(self, form, commit=True):

        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])

        if commit:
            user.save()
            current_site = get_current_site(self.request)
            subject = 'Activate your account'
            message = render_to_string('account/email_confirm.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_str(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
        return super().form_valid(form)


def activate(request, uid, token):
    try:
        _uid = force_str(urlsafe_base64_decode(uid))
        user = MyUser.objects.get(pk=_uid)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account/account_verification_invalid_notice.html')
