# -*- coding: utf-8 -*-
"""
bofhirdev
FILE: application
Created: 11/5/15 10:50 PM


"""
from django.conf import settings
from django.views.generic import (DetailView,
                                  UpdateView)
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from appmgmt.forms.application import ApplicationForm
from appmgmt.models import BBApplication


__author__ = 'Mark Scrimshire:@ekivemark'


class MyApplicationListView(ListView):
    """
    View for Applications

    """
    model = BBApplication
    template_name = 'appmgmt/application_list.html'

    def get_queryset(self):
        if settings.DEBUG:
            print("Queryset User:", self.request.user)
        qs = super(MyApplicationListView, self).get_queryset()
        return qs.filter(user=self.request.user).values()

# Application Create


# Application Update


# Application Delete
class MyApplicationUpdateView(UpdateView):
    """
    Edit view for Application

    """
    model = BBApplication
    fields = ['name', 'about',
              'privacy_url', 'support_url',
              'redirect_uris' , 'client_type',
              'logo',]

    context_object_name = "application"

    def get_context_data(self, **kwargs):
        # call the base implementation first to get a context
        context = super(MyApplicationUpdateView, self).get_context_data(**kwargs)
        # add in a QuerySet of all Applications
        if settings.DEBUG:
            print("Context:", context)

        return context


class MyApplicationCreate(CreateView):
    """
    Create for Application
    """

    model = BBApplication
    form_class = ApplicationForm
    fields = ['name', 'about',
              'logo', 'privacy_url', 'support_url',
              'redirect_uris', 'client_type']

    def get_initial(self):
        self.initial.update({ 'owner': self.request.user})
        return self.initial

# Organization Update



