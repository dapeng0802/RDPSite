#--coding=utf-8--

from django.contrib.auth.backends import ModelBackend
from RDPSite.models import SiteUser

class EmailAuthBackend(ModelBackend):
    
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = SiteUser.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except SiteUser.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return SiteUser.objects.get(pk=user_id)
        except SiteUser.DoesNotExist:
            return None
