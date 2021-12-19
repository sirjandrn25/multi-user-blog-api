from blog.serializers.posts import PostDetailSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..permissions import IsPostOwnerOrIsAdmin,IsAdminOrReadOnly
from ..models.post import Post,Category,Comment
from ..serializers import PostSerializer,UserSerializer,CommentSerializer,CategorySerializer
from .paginations import MyPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers
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
    # parser_classes = [JSONParser,MultiPartParser,FormParser]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['category','tutorial']
    search_fields = ['title', 'description','user__username']

    pagination_class = MyPageNumberPagination

        
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self,request,pk):
        post = self.get_object()
        post.views +=1
        post.save()
        
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)




    def create(self,request):

        # return Response()
        serializer = PostSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)

            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    
    @action(detail=True, methods=['put'])
    def update_thumbnail(self,request,pk=None):
        post = get_object_or_404(Post.objects.all(),pk=pk)
        serializer = PostSerializer(data=request.data,instance=post,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response()
        return Response(serializer.errors,status=400)
    
    @action(detail=False,methods=['get'])
    def top_posts(self,request,pk=None):
        
        posts = Post.objects.filter(id__range=[len(self.queryset)-4,len(self.queryset)])
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
    

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
        
        users = post.likes.all()
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