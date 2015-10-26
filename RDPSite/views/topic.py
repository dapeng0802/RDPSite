#--coding:utf-8--

from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from RDPSite.models import SiteUser, Plane, Node, Topic, Reply, Favorite, Notification, Transaction, Vote 

def get_index(request):
    user = request.user
    if user.is_authenticated():
        counter = {
            'topics': user.topic_author.all().count(),
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

def get_user_replies(request, uid):
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
        'favorites': user_info.fav_user.all().count
        
    }
    
    user =request.user
    if user.is_authenticated():
        notification_count = user.notify_user.filter(status=0).count()
        
    replies, reply_page = Reply.objects.get_user_all_replies(user_info.id, current_page=current_page)
    active_page = 'topic'
    return render_to_response('topic/user_replies.html', locals(), context_instance=RequestContext(request))

def get_user_favorites(request, uid):
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
        notification_count = user.notify_user.filter(status=0).count()
        
    favorites, favorite_page = Favorite.objects.get_user_all_favorites(user_info.id, current_page=current_page)
    avtive_page = 'topic'
    return render_to_response('topic/user_favorites.html', locals(), context_instance=RequestContext(request))

def get_members(request):
    user = request.user
    if user.is_authenticated():
        counter = {
            'topics': user.topic_author.all().count(),
            'replies': user.reply_author.all().count(),
            'favorites': user.fav_user.all().count()
        }
        notification_count = user.notify_user.filter(status=0).count()
    
    members = SiteUser.objects.all().order_by('-id')[:49]
    active_members = SiteUser.objects.all().order_by('-last_login')[:49]
    active_page = 'members'
    return render_to_response('topic/members.html', locals(), context_instance=RequestContext(request))

def get_node_topics(request, slug):
    node = get_object_or_404(Node, slug=slug)
    
    user = request.user
    if user.is_authenticated():
        counter = {
            'topics': user.topic_author.all().count(),
            'replies': user.reply_author.all().count(),
            'favorites': user.fav_user.all().count()
        }
        notification_count = user.notify_user.filter(status=0).count()
    
    try:
        current_page = int(request.GET.get('p', '1'))
    except ValueError:
        current_page = 1
    
    topics, topic_page = Topic.objects.get_all_topics_by_slug(current_page=current_page, node_slug=slug)
    active_page = 'topic'
    return render_to_response('topic/node_topics.html', locals(), context_instance=RequestContext(request))