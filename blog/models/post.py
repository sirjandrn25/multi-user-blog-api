from django.db import models
from .user import User


class DateTimePicker(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering=['-id']


class Category(models.Model):
    c_name = models.CharField(max_length=150)
    
    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        return self.c_name
        

class Tutorial(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="tutorials")

    def __str__(self):
        return self.name
    

class Post(DateTimePicker):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    body = models.TextField()
    thumbnail = models.ImageField(upload_to="posts",blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="posts")
    likes = models.ManyToManyField(User,blank=True,related_name="likes")
    views = models.IntegerField(default=0)
    tutorial = models.ForeignKey(Tutorial,on_delete=models.CASCADE,related_name="posts",null=True)

    def __str__(self):
        return self.title
    
    @staticmethod
    def autocomplete_search_fields():
        return 'title', 'user__name'
    class Meta:
        ordering = ['-id']

    



class Comment(DateTimePicker):
    content = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")

    class Meta:
        ordering = ['id']

    

class Reply(DateTimePicker):
    content = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="replies")
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="replies")
    class Meta:
        ordering = ['id']
