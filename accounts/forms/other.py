"""
accounts
FILE: forms.py
Created: 6/21/15 8:31 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
from registration.forms import (RegistrationFormUniqueEmail,
                                RegistrationFormTermsOfService)

from accounts.models import User

class Email(forms.EmailField):
    def clean(self, value):
        if settings.DEBUG:
            print("email is ", value)
        value = value.lower()
        super(Email, self).clean(value)
        try:
            User.objects.get(email=value)
            raise forms.ValidationError(mark_safe(
                "This email is already registered. <br/>Use <a href='/password/reset'>this forgot password</a> link or on the <a href ='/accounts/login?next=/'>login page</a>."))
        except User.DoesNotExist:
            if settings.DEBUG:
                print("no match on user:", value)
            return value


class UserRegistrationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    # email will be become username
    email = Email()

    password1 = forms.CharField(widget=forms.PasswordInput(),
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(),
                                label="Repeat your password")

    fields = ['user', 'email', 'password1', 'password2' ]

    def clean_user(self):
        """
        We need to check that user is not containing spaces.
        We also need to make sure it is lower case

        :return: self
        """

        data = self.cleaned_data['user']
        # remove spaces
        data = data.replace(" ", "")
        # Convert to lowercase
        data = data.lower()
        if data == "":
            raise forms.ValidationError("User name is required")

        if settings.DEBUG:
            print("User: ",  self.cleaned_data['user'], " = [",data, "]" )

        return data

    def clean_password(self):
        if self.data['password1'] != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password1']


class RegistrationFormUserTOSAndEmail(UserRegistrationForm,
                                      RegistrationFormUniqueEmail,
                                      RegistrationFormTermsOfService,
                                      ):

    class Meta:
        model = User
        fields = ['user',
                  'email',
                  'first_name',
                  'last_name']
        # exclude = ['user']
    # pass


class RegistrationFormTOSAndEmail(
    RegistrationFormUniqueEmail,
    RegistrationFormTermsOfService,
    ):

    pass
