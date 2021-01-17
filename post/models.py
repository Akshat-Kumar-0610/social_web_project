from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.urls import reverse

class post(models.Model):
    title=models.CharField(max_length=200)
    image_post =models.ImageField(null= True, blank = True,upload_to='images/')
    content=models.TextField()
    Date=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='author')
    like =models.ManyToManyField(User,related_name='like',blank=True,verbose_name='liked_by')
    dislike =models.ManyToManyField(User,related_name='dislike',blank=True,verbose_name='disliked_by')
    class Meta:
        ordering = ['-Date']


    def total_likes(self):
        self.like.count()
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post',kwargs={'pk':self.pk})

class Comment(models.Model):
    post=models.ForeignKey(post,related_name='comments', on_delete=models.CASCADE,verbose_name='post')
    name=models.CharField(max_length=250 , null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='commented_by')
    body=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

    class Meta:
        ordering = ['-date_added']

    

        
