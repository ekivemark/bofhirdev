# -*- coding: utf-8 -*-
"""
bofhirdev
FILE: urls
Created: 10/29/15 8:04 AM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy

from appmgmt.views.application import (MyApplicationListView,
                                       MyApplicationUpdateView,
                                       Application_Update_Secret)
from appmgmt.views.organization import (MyOrganizationListView,
                                        MyOrganizationUpdateView,
                                        MyOrganizationCreate,
                                       )
# from appmgmt.views.trust import (TrustData)

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'bofhirdev.views.home', name='home'),

                       url(r'^myorganizations/$',
                           MyOrganizationListView.as_view(),
                           name='organization_view'),
                       url(r'^createorganization/$',
                           MyOrganizationCreate.as_view(success_url=reverse_lazy('accounts:manage_account')),
                           name='organization_create'),
                       url(r'^updateorganization/(?P<pk>[0-9]+)/$',
                           MyOrganizationUpdateView.as_view(success_url=reverse_lazy('appmgmt:organization_view')),
                           name='organization_update'),

                       url(r'^trustdata/$', 'appmgmt.views.trust.TrustData',
                           name='trustdata'),

                       url(r'^myapplications/$',
                           MyApplicationListView.as_view(),
                           name='application_view'),
                       url(r'^updateapplication/(?P<pk>[0-9]+)/$',
                           MyApplicationUpdateView.as_view(success_url=reverse_lazy('appmgmt:application_view')),
                           name='application_update'),
                       url(r'^updateapplicationsecret/(?P<pk>[0-9]+)/$',
                           'appmgmt.views.application.Application_Update_Secret',
                           name='application_update_secret'),

                       url(r'^trustcheck/(?P<requester_email>.+)/(?P<bundle>.+)/(?P<domain>.+)/(?P<owner_email>.+)$',
                           'appmgmt.views.trust.BaseTrust',
                           name='trustcheck'),

                       url(r'^trust_test/$',
                           'appmgmt.views.trust.TrustTest',
                           name='trusttest'),
                       )
