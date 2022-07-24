from ..models.post import *
from rest_framework import request, serializers

from django.contrib.auth.hashers import check_password,make_password
from django.db.models import Q
from .users import UserSerializer



class ReplySerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()
    def get_user_detail(self,obj):
        user = User.objects.get(id=obj.user.id)
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
        
        data = {
            'id':None,
            'user_types':obj.user_types,
            'username':obj.full_name,
            'email':obj.email
        }
        if obj.user:
            user = User.objects.filter(id=obj.user.id).first()
            avatar=''
            if user.profile.avatar:
                avatar = user.profile.avatar.url
            username = obj.user.profile.first_name + ' ' + obj.user.profile.last_name
            if username:
                username = obj.user.username
                
            data['username'] = username
            data['avatar'] = avatar
            data['id'] = obj.user.id
            
        
        return data



    class Meta:
        model = Comment
        fields = ['id','content','created_at','post','user_detail','replies','full_name','email','is_visible']
        read_only_fields = ["id",'user_detail','replies']
        extra_kwargs = {
            'full_name':{'write_only':True},
            'email':{'write_only':True}
        }

    def create(self,validated_data):
        return Comment.objects.create(**validated_data)