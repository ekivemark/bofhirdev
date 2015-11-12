"""
bofhirdev.apps.appmgmt
FILE: views.py
Created: 10/28/15 5:20pm

"""

import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.http import (HttpResponse,
                         JsonResponse,
                         HttpResponseRedirect)
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import (DetailView,
                                  UpdateView)
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from appmgmt.models import (Organization, BBApplication)
from appmgmt.forms import OrganizationForm

# We need an app management set of transactions here

# Organization Display
class MyOrganizationListView(ListView):
    """
    View for Organizations

    :param ListView:
    :return:
    """

    model = Organization
    template_name = 'appmgmt/organization_list.html'

    def get_queryset(self):
        if settings.DEBUG:
            print("Queryset User:", self.request.user)
        qs = super(MyOrganizationListView, self).get_queryset()

        if settings.DEBUG:
            result = qs.filter(owner=self.request.user).values()
            print("qs filter:", result)
            print("Developers:", qs[0].developers)

        return qs.filter(owner=self.request.user).values()
    # def get_context_data(self, **kwargs):
    #     context = super(MyOrganizationListView, self).get_context_data(**kwargs)


class MyOrganizationUpdateView(UpdateView):
    """
    Edit view for Organization

    """
    model = Organization
    fields = ['name', 'domain', 'developers']

    context_object_name = "organization"

    def get_context_data(self, **kwargs):
        # call the base implementation first to get a context
        context = super(MyOrganizationUpdateView, self).get_context_data(**kwargs)
        # add in a QuerySet of all Applications
        context['extra_content'] = {"application_list":BBApplication.objects.filter(organization=self.kwargs['pk'])}
        if settings.DEBUG:
            print("Context:", context)

        return context


class MyOrganizationCreate(CreateView):
    """
    Create for Organization
    """

    model = Organization
    form_class = OrganizationForm
    # fields = ['name', 'domain', 'developers',]

    def get_initial(self):
        self.initial.update({ 'owner': self.request.user})
        return self.initial

# Organization Update


