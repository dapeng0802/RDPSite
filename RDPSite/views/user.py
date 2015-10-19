#--coding:utf-8--

import os, uuid, copy
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Context, loader
from django.contrib import auth
from RDPSite.forms.user import RegisterForm, LoginForm, ForgotPasswordForm, SettingForm
from django.conf import settings
from common import sendmail
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

def get_forgotpassword(request, **kwargs):
    auth.logout(request)
    return render_to_response('user/forgot_password.html', kwargs, context_instance=RequestContext(request))

def post_forgotpassword(request):
    form = ForgotPasswordForm(request.POST)
    if not form.is_valid():
        return get_login(request, errors=form.errors)
    
    user = form.get_user()
    
    new_password = uuid.uuid1().hex
    user.set_password(new_password)
    user.updated = timezone.now()
    user.save()
    
    # 给用户发送新密码
    mail_title = u'RDPSite 找回密码'
    var = {'email': user.email, 'new_password': new_password}
    mail_content = loader.render_to_string('user/forgot_password_mail.html', var)
    sendmail(mail_title, mail_content, user.email)
    
    return get_forgotpassword(request, success_message=u'新密码已发送至您的注册邮箱')

@login_required
def get_setting(request, **kwargs):
    return render_to_response('user/setting.html', kwargs, context_instance=RequestContext(request))

@login_required
def post_setting(request):
    form = SettingForm(request.POST)
    if not form.is_valid():
        return get_setting(request, errors=form.errors)
    
    user = request.user
    cd = copy.copy(form.cleaned_data)
    cd.pop('username')
    cd.pop('email')
    for k, v in cd.iteritems():
        setattr(user, k, v)
    user.updated = timezone.now()
    user.save()
    return get_setting(request, success_message=u'用户基本资料更新成功')