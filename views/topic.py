#--coding:utf-8--

from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def get_index(request):
    # locals()返回一个包含当前作用域里面的所有变量和它们的值的字典。
    return render_to_response('test.html', locals(), context_instance=RequestContext(request))