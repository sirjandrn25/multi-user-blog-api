from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..permissions import IsPostOwnerOrCommentOwnerOrIsAdmin,IsPostOwnerOrReplyOwnerOrIsAdmin
from ..serializers import CommentSerializer,ReplySerializer
from ..models.post import Comment,Reply
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .paginations import MyPageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action



class CommentApiView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsPostOwnerOrCommentOwnerOrIsAdmin]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['post','user__username']
    pagination_class = MyPageNumberPagination
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj


    @action(detail=True,methods=['put'],permission_classes=[IsAuthenticatedOrReadOnly])
    def update_visible(self,request,pk):
        comment = self.get_object()
        if comment.post.user == request.user:
            comment.is_visible = (not comment.is_visible)
            comment.save()
            return Response()

        return Response(status=401)

    # add current user
    # def get_serializer(self,*args,**kwargs):
    #     kwarg_list = list(kwargs.keys())
    #     if kwargs.keys() and 'many' not in kwarg_list:
    #         # kwargs['data']._mutable = True
    #         if self.request.method == 'POST':
    #             try:
    #                 kwargs['data']['user'] = self.request.user.id
    #             except Exception as e:
                
    #                 kwargs['data']._mutable = True
    #                 kwargs['data']['user'] = self.request.user.id
    #         else:
    #             obj = self.get_object()
    #             kwargs['data']['user'] = obj.user.id
    #     return super(CommentApiView,self).get_serializer(*args,**kwargs)

    

    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if request.user.is_authenticated:
                serializer.save(user=request.user,user_types="regular")
            else:
                serializer.save(user_types="guest")
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    
    
    
    @action(detail=True,methods=['get'])
    def replies(self,request,pk=None):
        comment = get_object_or_404(Comment.objects.all(),pk=pk)
        replies = Reply.objects.filter(comment=comment)
        serializer = ReplySerializer(replies,many=True)
        return Response(serializer.data)
    


    

class ReplyApiView(ModelViewSet):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsPostOwnerOrReplyOwnerOrIsAdmin]
    pagination_class = MyPageNumberPagination
    def get_object(self):
        
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    # def get_serializer(self,*args,**kwargs):
    #     kwarg_list = list(kwargs.keys())
    #     if kwargs.keys() and 'many' not in kwarg_list:
    #         # kwargs['data']._mutable = True
    #         if self.request.method == 'POST':
    #             try:
    #                 kwargs['data']['user'] = self.request.user.id
    #             except Exception as e:
    #                 print(e)
    #                 kwargs['data']._mutable = True
    #                 kwargs['data']['user'] = self.request.user.id
                
    #         else:
    #             obj = self.get_object()
    #             kwargs['data']['user'] = obj.user.id
    #     return super(ReplyApiView,self).get_serializer(*args,**kwargs)
    

