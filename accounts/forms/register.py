"""
developeraccount
FILE: register
Created: 6/22/15 12:31 PM

Remember to add new classes to accounts.forms.__init__.py

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django import forms
from django.conf import settings

from accounts.models import User


class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new account.
    """
    user = forms.CharField(label="Username")
    email = forms.EmailField(widget=forms.EmailInput, label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Password (again)")
    first_name = forms.CharField(max_length=50,
                                 widget=forms.TextInput,
                                 label="First name")
    last_name = forms.CharField(max_length=50,
                                widget=forms.TextInput,
                                label="Last name")

    class Meta:
        model = User
        fields = ['email',
                  'password1', 'password2',
                  'first_name', 'last_name',
                  'user']

    def clean_user(self):
        """
        We need to check that user is not containing spaces.
        We also need to make sure it is lower case

        :return: self
        """

        data = self.cleaned_data['user']
        # remove spaces
        data = data.strip()
        # Convert to lowercase
        data = data.lower()
        if data == "":
            raise forms.ValidationError("User name is required")

        if settings.DEBUG:
            print("User: ",  self.cleaned_data['user'], " = [",data, "]" )

        return data

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        cleaned_data = super(RegistrationForm, self).clean()

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data[
                'password2']:
                raise forms.ValidationError(
                    "Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
