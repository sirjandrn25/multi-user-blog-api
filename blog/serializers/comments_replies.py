from ..models.post import *
from rest_framework import serializers

from django.contrib.auth.hashers import check_password,make_password
from django.db.models import Q



class ReplySerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()

        

    def get_user_detail(self,obj):
        user = User.objects.get(id=obj.user.id)
        serializer = UserSerializer(user,many=False)
        return serializer.data
    
    class Meta:
        model = Reply
        fields = ['id','content','created_at','comment','user','user_detail']
        read_only_fields = ['id','user_detail']


    

    

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user_detail = serializers.SerializerMethodField()
    
    def get_replies(self,obj):
        replies = Reply.objects.filter(comment=obj)
        return len(replies)

    def get_user_detail(self,obj):
        user = User.objects.get(id=obj.user.id)
        serializer = UserSerializer(user,many=False)
        return serializer.data
   
    class Meta:
        model = Comment
        fields = ['id','content','created_at','post','user','user_detail','replies']
        read_only_fields = ["id",'user_detail','replies']