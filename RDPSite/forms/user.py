#--coding=utf-8--

from django import forms
from RDPSite.models import SiteUser
from django.conf import settings 

error_messages = {
    'username': {
        'required': u'必须填写用户名',
        'min_length': u'用户名长度过短（3-12个字符）',
        'max_length': u'用户名长度过长（3-12个字符）',
        'invalid': u'用户名格式错误（英文字母开头，数字，下划线构成）'
    },
    'email': {
        'required': u'必须填写E-mail',
        'min_length': u'Email长度有误',
        'max_length': u'Email长度有误',
        'invalid': u'Email地址无效'
    },
    'password': {
        'required': u'必须填写密码',
        'min_length': u'密码长度过短（6-64个字符）',
        'max_length': u'密码长度过长（6-64个字符）'
    },
}

class RegisterForm(forms.ModelForm):
    username = forms.RegexField(min_length=3, max_length=12, regex=r'^[a-zA-Z][a-zA-Z0-9]*$', error_message=error_messages.get('username'))
    email = forms.EmailField(min_length=4, max_length=64, error_messages=error_messages.get('email'))
    password = forms.CharField(min_length=6, max_length=64, error_messages=error_messages.get('password'))
    password_confirm = forms.CharField(required=False)
    
    class Meta:
        model = SiteUser
        fields = ('username', 'email')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            SiteUser.objects.get(username=username)
            raise forms.ValidationError(u'所填用户名已被注册')
        except SiteUser.DoesNotExist:
            if username in settings.RESERVED:
                raise forms.ValidationError(u'所填用户名为系统保留关键字，不可用')
            return username
    def clean_emial(self):
        email = self.cleaned_data['email']
        try:
            SiteUser.objects.get(email=email)
            raise forms.ValidationError(u'所填邮箱已被注册')
        except SiteUser.DoesNotExist:
            return email