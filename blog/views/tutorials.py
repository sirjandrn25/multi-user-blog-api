from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..serializers import TutorialSerializer,AddRemovePostInTutorial
from ..models.post import Tutorial,Post
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsOwnUserOrIsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .paginations import MyPageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action



class TutorialApiView(ModelViewSet):
    serializer_class = TutorialSerializer
    queryset = Tutorial.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsOwnUserOrIsAdmin]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['user']
    search_fields=['name']
    pagination_class = MyPageNumberPagination
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self,request):
        tutorials = Tutorial.objects.filter(user=request.user)
        serializer = TutorialSerializer(tutorials,many=True)
        return Response(serializer.data,status=200)
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    
    @action(detail=True,methods=['put'],serializer_class=AddRemovePostInTutorial)
    def add_posts(self,request,pk=None):

        tutorial = Tutorial.objects.filter(id=pk).first()
        if not tutorial:
            return Response({"detail":"not found"},status=404)
        serializer = AddRemovePostInTutorial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            for post in serializer.validated_data.get('posts'):
                if post.user != request.user:
                    return Response({"detail":f"{post.id} this post id not allowed to add"})
                tutorial.posts.add(post)
            
            return Response()
        return Response(serializer.errors,status=400)

        
        
    
    @action(detail=True,methods=['put'],serializer_class=AddRemovePostInTutorial)
    def remove_posts(self,request,pk=True):
        tutorial = Tutorial.objects.filter(id=pk).first()
        if not tutorial:
            return Response({"detail":"not found"},status=404)
        serializer = AddRemovePostInTutorial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            for post in serializer.validated_data.get('posts'):
                if post in tutorial.posts.all():
                    tutorial.posts.remove(post)
            return Response(status=204)
                
        return Response({"detail":"not found"},status=404)
        
