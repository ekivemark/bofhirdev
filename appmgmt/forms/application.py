# -*- coding: utf-8 -*-
"""
bofhirdev
FILE: application
Created: 11/2/15 9:34 AM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django import forms
from django.conf import settings

from appmgmt.models import BBApplication

class ApplicationForm(forms.ModelForm):
    """
    Model  form for BBApplication with request.user override
    """
    class Meta:
        model = BBApplication
        fields = ['name', 'logo', 'privacy_url', 'support_url' ]

    def __init__(self, *args, **kwargs):
        self.owner = kwargs['initial']['owner']
        super(ApplicationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(ApplicationForm, self).save(False)
        obj.owner = self.owner
        commit and obj.save()
        return obj
