from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..permissions import IsPostOwnerOrIsAdmin,IsAdminOrReadOnly
from ..models.post import Post,Category,Comment
from ..serializers import PostSerializer,UserSerializer,CommentSerializer,CategorySerializer
from .paginations import MyPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response


class PostApiView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsPostOwnerOrIsAdmin]

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = [JSONParser,MultiPartParser,FormParser]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['category','tutorial']
    search_fields = ['title', 'description','user__username']

    pagination_class = MyPageNumberPagination

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj


    def get_serializer(self,*args,**kwargs):
        kwarg_list = list(kwargs.keys())
        
        
        if kwargs.keys() and 'many' not in kwarg_list:
            # kwargs['data']._mutable = True
            if self.request.method == 'POST':
                try:
                    kwargs['data']['user'] = self.request.user.id
                except Exception as e:
                    print(e)
                    kwargs['data']._mutable = True
                    kwargs['data']['user'] = self.request.user.id
            else:
                obj = self.get_object()
                
                kwargs['data']['user'] = obj.user.id
        return super(PostApiView,self).get_serializer(*args,**kwargs)

    @action(detail=True, methods=['put','get'])
    def likes(self,request,pk=None):
        post = get_object_or_404(Post.objects.all(),pk=pk)
        if request.method == 'PUT':
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                return Response(status=204)
            else:
                post.likes.add(request.user)
                return Response(status=200)
        elif request.method == 'GET':
            users = post.likes.all()
            serializer = UserSerializer(users,many=True)
            return Response(serializer.data)
        
    
    @action(detail=True, methods=['put','get'])
    def views(self,request,pk=None):

        post = get_object_or_404(Post.objects.all(),pk=pk)

        if request.method == 'PUT':
            post.views.add(request.user)
            return Response(status=200)
        elif request.method == 'GET':
            users = post.views.all()
            serializer = UserSerializer(users,many=True)
            return Response(serializer.data)
    
    
    
    @action(detail=True,methods=['get'])
    def comments(self,request,pk=None):
        post = get_object_or_404(Post.objects.all(),pk=pk)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data,status=200)



class CategoryApiView(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsAdminOrReadOnly]