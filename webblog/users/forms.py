from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import fields, widgets
from django.utils.translation import gettext_lazy as _

from .models import MyUser


class UserCreationFrom(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'name', 'date_of_birth',
                  'picture', 'is_staff', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Password don't match!"))

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'name', 'date_of_birth',
                  'picture', 'is_staff', 'is_superuser')


class UserSignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password', widget=widgets.PasswordInput)
    password2 = forms.CharField(
        label='Password Confirmation', widget=widgets.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'name')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Password don't match!"))
        return password2
