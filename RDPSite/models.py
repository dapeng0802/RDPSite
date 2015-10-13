#--coding:utf-8--

from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL.ImageFont import truetype
from django.db.models.sql.query import Query

# 工具
class Pages(object):
    '''
    分页查询类
    '''
    def __init__(self, count, current_page=1, list_rows=40):
        self.total = count
        self._current = current_page
        self.size = list_rows
        self.pages = self.total // self.size + (1 if self.total % self.size else 0)
        
        if (self.pages == 0) or (self._current < 1) or (self._current > self.pages):
            self.start = 0
            self.end = 0
            self.index = 1
        else:
            self.start = (self._current - 1) * self.size
            self.end = self.start + self.size
            self.index = self._current
        self.prev = self.index - 1 if self.index > 1 else self.index
        self.next = self.index + 1 if self.index < self.pages else self.index

# 数据库字段类型定义
class NormalTextField(models.TextField):
    '''
    models.TextField 默认在MySQL上的数据类型是longtext，用不到那么大，
    所以派生NormalTextField，只修改生成SQL时的数据类型text
    '''
    def db_type(self, connection):
        return 'text'

class NodeManager(models.Manager):
    '''
    Node objects
    '''
    def get_all_hot_nodes(self):
        query = self.get_query_set().filter(topic__reply_count__gt=0).order_by('-topic__reply_count')
        query.query.group_by = ['id']
        return query

class TopicManager(models.Manager):
    '''
    Topic objects
    '''
    def get_all_topic(self, num=36, current_page=1):
        count = self.get_query_set().count()
        page = Pages(count, current_page, num)
        query = self.get_query_set().select_related('node', 'author', 'last_replied_by').\
            all().order_by('-last_touched', '-created', '-last_replied_time', '-id')[page.start:page.end]
        return query, page
    
    def get_all_topics_by_slug(self, num=36, current_page=1, node_slug=None):
        count = self.get_query_set().filter(node__slug=node_slug).count
        page = Pages(count, current_page, num)
        query = self.get_query_set().select_related('node', 'author', 'last_replied_by').\
            filter(node__slug=node_slug).order_by('-last_touched', '-created', '-last_replied_time', '-id')[page.start:page.end]
        return query, page

    def get_user_all_topics(self, uid, num=36, current_page=1):
        count = self.get_query_set().filter(author__id=uid).count()
        page = Pages(count, current_page, num)
        query = self.get_query_set().select_related('topic').filter(author__id=uid).order_by('-id')[page.start:page.end]
        return query, page
    
    def get_topic_by_topic_id(self, topic_id):
        query = self.get_query_set().select_related('node', 'author', 'last_replied_by').get(pk=topic_id)
        return query    
        
    def get_user_last_created_topic(self, uid):
        query = self.get_query_set().filter(author__id=uid).order_by('created')[0]
        return query

class ReplyManager(models.Manager):
    '''
    Reply objects
    '''
    def ger_all_replies_by_topic_id(self, topic_id, num=16, current_page=1):
        count = self.get_query_set().filter(topic__id=topic_id).count()
        page = Pages(count, current_page, num)
        query = self.get_query_set().select_related('author').filter(topic__id=topic_id).order_by('id')[page.start:page.end]
        return query, page
    
    def get_user_all_replies(self, uid, num=16, current_page=1):
        count = self.get_query_set().filter(author__id=uid).count()
        page = Pages(count, current_page, num)
        query = self.get_query_set().select_related('topic', 'topic__author').\
            filter(author__id=uid).order_by('-id')[page.start:page.end]
        return query, page

class FavoriteManager(models.Manager):
    '''
    Favorite objects
    '''
    def get_user_all_favorites(self, uid, num=16, current_page=1):
        count = self.get_query_set().filter(owner_user__id=uid).count()
        page = Pages(count, current_page, num)
        query = self.get_query_set().select_related('involved_topic', 'involved_topic__node','involved_topic__author',\
                                                    'involved_topic__last_replied_by').filter(owner_user__id=uid).\
                                                    order_by('-id')[page.start:page.end]
        return query, page

class NotificationManager(models.Manager):
    '''
    Notification objects
    '''
    def get_user_all_notifications(self, uid, num=16, current_page=1):
        count = self.get_query_set().filter(involved_user__id=uid).count()
        page = Pages(count, current_page, num)
        query = self.get_query_set().select_related('trigger_user', 'involved_topic').filter(involved_user__id=uid).\
            order_by('-id')[page.start:page.end]
        return query, page

# 数据库表结构
class SiteUser(AbstractUser):
    '''
    django.contrib.auth.models.User 默认User类字段太少，用AbstractUser自定义一个User类，增加字段
    '''
    # 昵称
    nickname = models.CharField(max_length=200, null=True, blank=True)
    # 头像
    avatar = models.CharField(max_length=200, null=True, blank=True)
    # 签名
    signature = models.CharField(max_length=500, null=True, blank=True)
    # 位置
    location = models.CharField(max_length=200, null=True, blank=True)
    # 网站
    website = models.URLField(null=True, blank=True)
    # 公司
    company = models.CharField(max_length=200, null=True, blank=True)
    # 角色
    role = models.IntegerField(null=True, blank=True)
    # 余额
    balance = models.IntegerField(null=True, blank=True)
    # 声誉
    reputation = models.IntegerField(null=True, blank=True)
    # 自我介绍
    slef_intro = models.CharField(max_length=500,  null=True, blank=True)
    # 更新时间
    updated = models.DateTimeField(null=True, blank=True)
    # 微博
    weibo = models.CharField(max_length=200, null=True, blank=True)
    # github
    github = models.CharField(max_length=200, null=True, blank=True)
    # 豆瓣
    douban = models.CharField(max_length=200, null=True, blank=True)

class Plane(models.Model):
    '''
    论坛节点分类
    '''
    name = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    
class Node(models.Model):
    '''
    论坛板块单位，节点
    '''
    name = models.CharField(max_length=200, null=True, blank=True)
    # 块，作为node的识别url
    slug = models.CharField(max_length=200, null=True, blank=True)
    thubm = models.CharField(max_length=200, null=True, blank=True)
    introduction = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    plane = models.ForeignKey(Plane, null=True, blank=True)
    topic_count = models.IntegerField(null=True, blank=True)
    custom_style = NormalTextField(null=True, blank=True)
    limit_reputation = models.IntegerField(null=True, blank=True)
    objects = NodeManager()

class Topic(models.Model):
    '''
    话题表，定义了论坛帖子的基本单位
    '''
