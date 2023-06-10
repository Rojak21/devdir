from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import uuid

# Create your models here.
class Profile(models.Model):
    id = models.UUIDField(default = uuid.uuid4, primary_key=True, unique=True, editable=False)
    user = models.OneToOneField(User,blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True , null=True )
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to='profiles/', default='profiles/user-default.png')
    social_github =  models.CharField(max_length=255, blank=True, null=True)
    social_twitter = models.CharField(max_length=255, blank=True, null=True)
    social_linkedin = models.CharField(max_length=255, blank=True, null=True)
    social_youtube = models.CharField(max_length=255, blank=True, null=True)
    social_website = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add= True )

    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        ordering = ['created']
    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url
    
class Message(models.Model):
    id = models.UUIDField(default = uuid.uuid4, primary_key=True, unique=True, editable=False)
    sender = models.ForeignKey('Profile',blank=True, null=True, on_delete=models.SET_NULL)
    recipient = models.ForeignKey('Profile',blank=True, null=True, on_delete=models.SET_NULL, related_name='messages')
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(blank=True, null=True, default=False)
    created = models.DateTimeField(auto_now_add= True )

    def __str__(self):
        return str(self.subject)
    
    class Meta:
        ordering = ['is_read','-created']
    
class Skill(models.Model):
    id = models.UUIDField(default = uuid.uuid4, primary_key=True, unique=True, editable=False)
    owner =models.ForeignKey('Profile',blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=255,blank=True, null=True)
    created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return str(self.name)
    





