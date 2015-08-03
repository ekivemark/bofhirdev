"""
developeraccount
FILE: user
Created: 7/6/15 9:39 PM


"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required

__author__ = 'Mark Scrimshire:@ekivemark'

from django.template import RequestContext
from accounts.models import (User,
                             Crosswalk)
from django.conf import settings

from django.views.generic.edit import *
from django.core.urlresolvers import *
from django.shortcuts import (render)

from accounts.forms.user import User_EditForm


@login_required()
def user_edit(request):
    if settings.DEBUG:
        print(request.user)
        print("Entering User Edit with:%s" % request.user.email)

    u = User.objects.get(email=request.user.email)
    if settings.DEBUG:
        print("User returned:", u, "[", u.first_name, " ", u.last_name,
              "]")

    form = User_EditForm(data=request.POST or None, instance=u)

    if request.POST:
        form = User_EditForm(request.POST)
        if form.is_valid():
            # form.save()
            if settings.DEBUG:
                print("Form is valid - current record:", u)

            u.first_name = form.cleaned_data['first_name']
            u.last_name = form.cleaned_data['last_name']
            u.mobile = form.cleaned_data['mobile']
            u.carrier = form.cleaned_data['carrier']
            u.mfa = form.cleaned_data['mfa']
            if settings.DEBUG:
                print("Updated to:", u)
            u.save()

            return HttpResponseRedirect(reverse('accounts:manage_account'),
                                        RequestContext(request))
        else:
            if settings.DEBUG:
                print("Form is invalid")

            messages.error(request, "There was an input problem.")
            return render(request, 'accounts/user_edit.html',
                          {'form': form})

    else:
        u = User.objects.get(email=request.user.email)
        if settings.DEBUG:
            print("in the get with User:", u.first_name, " ", u.last_name,
                  " ", u.mobile)
        form = User_EditForm(
            initial={'first_name': u.first_name, 'last_name': u.last_name,
                     'mobile': u.mobile, 'carrier': u.carrier,
                     'mfa': u.mfa})
        if settings.DEBUG:
            print("Not in the post in the get")
        return render(request, 'accounts/user_edit.html',
                      {'form': form,
                       'email': u.email})


@login_required()
def Get_ID(Look_for="UUID", Find_with=""):
    """

    :param Look_for: "ICODE" or "UUID"

    :param Find_with: Code to search for
    :return: Code or empty string

    Default is to look for UUID and return ICODE
    """
    if Find_with == "":
        # return blank if no code to search for
        return ""

    looking_for = ""
    if Look_for.upper() == "ICODE":
        looking_for = "ICODE"
    else:
        looking_for = "UUID"

    # We have a value type and value to search for and a

    lu = {}

    luv = ""
    result = ""

    if looking_for == "ICODE":
        try:
            luv = Crosswalk.objects.get(guid=Find_with)
            result = luv.hicn
        except Crosswalk.DoesNotExist:
            result = ""
    else:
        try:
            luv = Crosswalk.objects.get(hicn=Find_with)
            result = luv
        except Crosswalk.DoesNotExist:
            result = ""

    lu = {looking_for: result}
    if settings.DEBUG:
        print("lu returned:", lu)
    return lu
