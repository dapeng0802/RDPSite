#--coding:utf-8--
from django.conf.urls import patterns, include, url
from views import common, topic, user
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
admin.site.login = login_required(admin.site.login) # 设置admin登录的页面，settings.LOGIN_URL

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RDPSite.views.home', name='home'),
    # url(r'^RDPSite/', include('RDPSite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', common.splitter, {'GET': topic.get_index}),
    url(r'^register/$', common.splitter, {'GET': user.get_register, 'POST': user.post_register}),
    url(r'^login/$', common.splitter, {'GET': user.get_login, 'POST': user.post_login}),
    url(r'^logout/$', common.splitter, {'GET': user.get_logout}),
    url(r'^forgot/$', common.splitter, {'GET': user.get_forgotpassword, 'POST': user.post_forgotpassword}),
    url(r'^setting/$', common.splitter, {'GET': user.get_setting, 'POST': user.post_setting}),
    url(r'^setting/avatar/$', common.splitter, {'GET': user.get_setting_avatar, 'POST': user.post_setting_avatar}),
    url(r'^setting/password/$', common.splitter, {'GET': user.get_setting_password, 'POST': user.post_setting_password}),
    url(r'^u/(.*)/topics', common.splitter, {'GET': topic.get_user_topics}),
    url(r'^u/(.*)/favorites', common.splitter, {'GET': topic.get_profile}),
    url(r'^u/(.*)/$', common.splitter, {'GET': topic.get_profile}),
)
