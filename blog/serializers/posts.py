from ..models.post import *
from rest_framework import serializers

from django.contrib.auth.hashers import check_password,make_password
from .comments_replies import *



    
    
    




class PostSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(read_only=True,many=True)
    comments=serializers.SerializerMethodField()
    user_detail = serializers.SerializerMethodField()

    # def get_user(self,obj):
        
    def get_comments(self,obj):
        comments = Comment.objects.filter(post=obj)
        return len(comments)
    def get_user_detail(self,obj):
        user = User.objects.get(id=obj.user.id)
        serializer = UserSerializer(user,many=False)
        return serializer.data

    class Meta:
        model = Post
        fields = ['id','title','description','thumbnail','category','user','user_detail','comments','likes','views','created_at','updated_at']
        read_only_fields = ['id','user_detail','comments','created_at','updated_at','likes','views']
    
    
    

class TutorialSerializer(serializers.ModelSerializer):
    posts = PostSerializer(read_only=True,many=True)
    class Meta:
        model = Tutorial
        fields = "__all__"
        read_only_fields = ['id']



class CategorySerializer(serializers.ModelSerializer):
    # posts = PostSerializer(read_only=True,many=True)
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ['id']


