from ..models.post import *
from rest_framework import request, serializers

from django.contrib.auth.hashers import check_password,make_password
from django.db.models import Q
from .users import UserSerializer



class ReplySerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()

        

    def get_user_detail(self,obj):
        user = User.objects.get(id=obj.user.id)
        serializer = UserSerializer(user,many=False)
        avatar = ''
        if user.profile.avatar:
            avatar = user.profile.avatar.url
        data = {
            'id':user.id,
            'useraname':user.username,
            'avatar':avatar
        }
        return data
    
    class Meta:
        model = Reply
        fields = ['id','content','created_at','comment','user_detail']
        read_only_fields = ['id','user_detail']
    
    def create(self,validated_data):
        return Reply.objects.create(**validated_data)
        


    

    

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user_detail = serializers.SerializerMethodField()
    
    def get_replies(self,obj):
        replies = Reply.objects.filter(comment=obj)
        return len(replies)

    def get_user_detail(self,obj):
        user = User.objects.get(id=obj.user.id)
        avatar=''
        if user.profile.avatar:
            avatar = user.profile.avatar.url
        data = {
            'id':user.id,
            'useraname':user.username,
            'avatar':avatar
        }
        return data
   
    class Meta:
        model = Comment
        fields = ['id','content','created_at','post','user_detail','replies']
        read_only_fields = ["id",'user_detail','replies']

    def create(self,validated_data):
        return Comment.objects.create(**validated_data)