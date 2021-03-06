from drf_yasg.openapi import Response
from ..models.post import *
from rest_framework import serializers

from django.contrib.auth.hashers import check_password,make_password
from .comments_replies import *
from .users import UserSerializer
from ..models.user import Profile, User



class PostSerializer(serializers.ModelSerializer):
    
    comments=serializers.SerializerMethodField()
    user_detail = serializers.SerializerMethodField()
        
    def get_comments(self,obj):
        comments = Comment.objects.filter(post=obj)
        return len(comments)
    def get_user_detail(self,obj):
        user = User.objects.get(id=obj.user.id)
        avatar = ''
        if user.profile.avatar:
            avatar = user.profile.avatar.url
        data = {
            'id':user.id,
            'username':user.username,
            'avatar':avatar
        }
        
        return data

    class Meta:
        model = Post
        fields = ['id','title','description','thumbnail','category','user_detail','comments','likes','views','created_at','updated_at']
        read_only_fields = ['id','user_detail','comments','created_at','updated_at','likes','views']
    
    def create(self,validated_data):
        return Post.objects.create(**validated_data)
    
    

    
    
    

class TutorialSerializer(serializers.ModelSerializer):
    posts = PostSerializer(read_only=True,many=True)
    class Meta:
        model = Tutorial
        fields = "__all__"
        read_only_fields = ['id','user']

class AddRemovePostInTutorial(serializers.ModelSerializer):
    # post_ids = serializers.ListField(child=serializers.IntegerField(min_value=1,max_value=100))
    class Meta:
        model = Tutorial
        fields = ['posts']

    
    

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ['id']