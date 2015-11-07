#--coding:utf-8--
from django.conf.urls import patterns, include, url
from views import common, topic, user
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from RDPSite.views import notification
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
    url(r'^u/(.*)/replies/$', common.splitter, {'GET': topic.get_user_replies}),
    url(r'^u/(.*)/favorites', common.splitter, {'GET': topic.get_user_favorites}),
    url(r'^u/(.*)/$', common.splitter, {'GET': topic.get_profile}),
    url(r'^members/$', common.splitter, {'GET': topic.get_members}),
    url(r'^node/(.*)/$', common.splitter, {'GET': topic.get_node_topics}),
    url(r'^t/create/(.*)/$', common.splitter, {'GET': topic.get_create, 'POST': topic.post_create}),
    url(r'^t/(\d+)/$', common.splitter, {'GET': topic.get_view, 'POST': topic.post_view}),
    url(r'^favorite/$', common.splitter, {'GET': topic.get_favorite}),
    url(r'^unfavorite/$', common.splitter, {'GET': topic.get_cancel_favorite}),
    url(r'^vote/$', common.splitter, {'GET': topic.get_vote}),
    url(r'^notifications/$', common.splitter, {'GET': notification.get_list}),
    url(r'^t/edit/(.*)/$', common.splitter, {'GET': topic.get_edit, 'POST': topic.post_edit}),
    url(r'^reply/edit/(.*)/$', common.splitter, {'GET': topic.get_reply_edit, 'POST': topic.post_reply_edit}),
)
