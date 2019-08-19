from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
# Create your models here.

class Film(models.Model):
    title = models.CharField(max_length=200)
    image_url = models.CharField(max_length=150)
    video_id = models.CharField(max_length=50)
    kind = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, null=True)
    publish = models.DateTimeField()
    love = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    def get_absolute_url(self):
        return reverse('video:play_video',args=[self.video_id,self.id,self.kind])
    def get_video_link(self):
        return ('https://www.youtube.com/embed/'+self.video_id)
    class Meta:
        db_table = 'film'
        ordering=('-publish',)
    def __str__(self):
        return self.title
class user_filmlist(models.Model):
    userId=models.CharField(max_length=30,default='')
    filmList=models.CharField(max_length=500,default='')
    class Meta:
        db_table='user_filmlist'
    def __str__(self):
        return self.userId
class Comment(models.Model):
    film=models.ForeignKey(Film,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=200)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    published=models.BooleanField(default=True)
    class Meta:
        ordering=('-created',)
        db_table='Comment'
    def __str__(self):
        return self.name