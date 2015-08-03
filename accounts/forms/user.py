"""
developeraccount
FILE: user
Created: 7/6/15 10:16 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django import forms

from accounts.models import User


class User_EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'mobile',
                  'carrier',
                  'mfa', ]
