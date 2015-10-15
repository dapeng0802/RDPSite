#--coding:utf-8--

from django.shortcuts import render_to_response
from django.core.context_processors import request
from django.template.context import RequestContext
from django.contrib import auth

def get_register(request, **kwargs):
    auth.logout()
    return render_to_response('user/register.html', kwargs, context_instance=RequestContext(request))