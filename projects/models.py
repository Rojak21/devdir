from django.db import models
from users.models import Profile
import uuid

# Create your models here.
class Project(models.Model):
    id = models.UUIDField(default = uuid.uuid4, primary_key=True, unique=True, editable=False)
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete= models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(blank=True, null=True, default= 'default.png')
    demo_link = models.CharField(max_length=255, blank=True, null=True)
    source_link = models.CharField(max_length=255, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_count = models.IntegerField(default=0, blank=True)
    vote_ratio = models.IntegerField(default=0, blank=True)
    created = models.DateTimeField(auto_now_add= True )

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-vote_ratio','-created','title']
    
    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url
    

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ratio = (upVotes/totalVotes)*100
        self.vote_count = totalVotes
        self.vote_ratio = ratio
        self.save()
    @property
    def reviewers(self):
        reviewersset = self.review_set.all().value_set('owner__id',flat=True)
        return reviewersset
        
    
class Review(models.Model):
    VOTE_TYPE = (('up','up vote'),('down','down vote'))
    id = models.UUIDField(default = uuid.uuid4, primary_key=True, unique=True, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=255, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add= True )

    def __str__(self):
        return self.value
    
    class Meta:
        unique_together = [['owner','project']]

class Tag(models.Model):
    id = models.UUIDField(default = uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    created = models.DateTimeField(auto_now_add= True )

    def __str__(self):
        return self.name
    
