# -*- coding: utf-8 -*-
"""
bofhirdev
FILE: organization
Created: 11/2/15 9:34 AM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django import forms
from django.conf import settings

from appmgmt.models import Organization

class OrganizationForm(forms.ModelForm):
    """
    Model  form for Organization with request.user override
    """
    class Meta:
        model = Organization
        fields = ['name', 'domain', 'developers', ]

    def __init__(self, *args, **kwargs):
        self.owner = kwargs['initial']['owner']
        super(OrganizationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(OrganizationForm, self).save(False)
        obj.owner = self.owner
        commit and obj.save()
        return obj
