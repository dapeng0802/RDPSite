#--coding:utf-8--

from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from RDPSite.models import SiteUser, Plane, Node, Topic, Reply, Favorite, Notification, Transaction, Vote 

def get_index(request):
    user = request.user
    if user.is_authenticated():
        counter = {
            'topic': user.topic_author.all().count(),
            'replies': user.reply_author.all().count(),
            'favorites': user.fav_user.all().count()
        }
        notifications_count = user.notify_user.filter(status=0).count()
    
    status_counter = {
        'users': SiteUser.objects.all().count(),
        'nodes': Node.objects.all().count(),
        'topics': Topic.objects.all().count(),
        'replies': Reply.objects.all().count(),
    }
    
    try:
        current_page = int(request.GET.get('p', '1'))
    except ValueError:
        current_page = 1
    
    topics, topic_page = Topic.objects.get_all_topic(current_page=current_page)
    planes = Plane.objects.prefetch_related('node_set')
    hot_nodes = Node.objects.get_all_hot_nodes()
    active_page = 'topic'
    # locals()返回一个包含当前作用域里面的所有变量和它们的值的字典。
    return render_to_response('topic/topics.html', locals(), context_instance=RequestContext(request))

def get_profile(request, uid):
    try:
        if uid.isdigit():
            user_info = SiteUser.objects.get(pk=uid)
        else:
            user_info = SiteUser.objects.get(username=uid)
    except SiteUser.DoesNotExist:
        raise Http404
    
    try:
        current_page = int(request.GET.get('p', '1'))
    except ValueError:
        current_page = 1
        
    counter = {
            'topics': user_info.topic_author.all().count(),
            'replies': user_info.reply_author.all().count(),
            'favorites': user_info.fav_user.all().count()
    }
    
    user = request.user
    if user.is_authenticated():
        notifications_count = user.notify_user.filter(status=0).count()
        
    topics, topic_page = Topic.objects.get_user_all_topics(user_info.id, current_page=current_page)
    replies, reply_page = Reply.objects.get_user_all_replies(user_info.id, current_page=current_page)
    active_page = '_blank'
    return render_to_response('topic/profile.html', locals(), context_instance=RequestContext(request))

def get_user_topics(request, uid):
    try:
        if uid.isdigit():
            user_info = SiteUser.objects.get(pk=uid)
        else:
            user_info = SiteUser.objects.get(username=uid)
    except SiteUser.DoesNotExist:
        raise Http404 
    
    try:
        current_page = int(request.GET.get('p', '1'))
    except ValueError:
        current_page = 1
    
    counter = {
               'topics': user_info.topic_author.all().count(),
               'replies': user_info.reply_author.all().count(),
               'favorites': user_info.fav_user.all().count()
    }
    
    user = request.user
    if user.is_authenticated():
        notifications_count = user.notify_user.filter(status=0).count()
    
    topics, topic_page = Topic.objects.get_user_all_topics(user_info.id, current_page=current_page)
    active_page = 'topic'
    return render_to_response('topic/user_topics.html', locals(), context_instance=RequestContext(request))
