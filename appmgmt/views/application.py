# -*- coding: utf-8 -*-
"""
bofhirdev
FILE: application
Created: 11/5/15 10:50 PM


"""
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import (DetailView,
                                  UpdateView)
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from oauth2_provider.generators import (generate_client_id,
                                        generate_client_secret)

from appmgmt.forms.application import (ApplicationForm,
                                       Application_Secret_Form,
                                       Application_Secret)
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


def Application_Update_Secret(request, pk):
    """
    Replace client_id and client_secret

    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        a=BBApplication.objects.get(pk=pk)
        form = Application_Secret(request.POST)

        if form.is_valid():
            if form.cleaned_data['confirm'] == '1':
                a.client_id = generate_client_id()
                a.client_secret = generate_client_secret()
                a.save()
                messages.success(request,"Client Id and Secret updated")

            if settings.DEBUG:
                print("Confirm:", form.cleaned_data['confirm'])
                print("Id:", a.client_id)
                print("Secret:", a.client_secret)

            return HttpResponseRedirect(reverse_lazy('appmgmt:application_view'))

        else:
            if settings.DEBUG:
                print("form has a problem")
    else:
        a=BBApplication.objects.get(pk=pk)
        if settings.DEBUG:
            print("BBApplication:", a)

        form = Application_Secret(initial={'confirm': '0'})
    return render_to_response('appmgmt/application_secret_form.html',
                              RequestContext(request,{'form': form, 'application': a,}))

