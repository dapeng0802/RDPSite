#--coding:utf-8--

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Context, loader
from django.contrib import auth
from RDPSite.forms.user import RegisterForm, LoginForm, error_messages
from django.conf import settings
from common import sendmail

def get_register(request, **kwargs):
    auth.logout(request)
    return render_to_response('user/register.html', kwargs, context_instance=RequestContext(request))

def post_register(request):
    form = RegisterForm(request.POST)
    
    if not form.is_valid():
        return get_register(request, errors=form.errors)
    
    user = form.save()
    if user:
        # 注册成功，发送邮件到用户邮箱
        mail_title = u'RDPSite 注册成功通知'
        #mail_content = loader.get_template('user/register_mail.html')
        mail_content = loader.render_to_string('user/register_mail.html',{})
        sendmail(mail_title, mail_content, user.email)
    return redirect(settings.LOGIN_URL)

def get_login(request, **kwargs):
    auth.logout(request)
    return render_to_response('user/login.html', kwargs, context_instance=RequestContext(request))

def post_login(request):
    form = LoginForm(request.POST)
    if not form.is_valid():
        return get_login(request, errors=form.errors)
    
    user = form.get_user()
    auth.login(request, user)
    
    if user.is_staff:
        return redirect(request.REQUEST.get('next', '/manage/admin/'))
    
    return redirect(request.REQUEST.get('next', '/'))

def get_logout(request):
    auth.logout(request)
    return redirect(request.REQUEST.get('next', '/'))