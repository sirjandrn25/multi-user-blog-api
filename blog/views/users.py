from blog.serializers.users import PassworChangeSerializer, UpdateAvatarSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from ..models.user import Profile,User
from ..serializers import UserSerializer,UserLoginSerializer,UserRegisterSerializer,ProfileSerializer,RefreshTokenSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from ..permissions import IsOwnUserOrIsAdmin
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


class UserApiView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnUserOrIsAdmin]
    

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    
    @action(detail=True, methods=['put'])
    @parser_classes([MultiPartParser,FormParser])
    def profile(self,request,pk=None):
        user = self.get_object()
      
        serializer = ProfileSerializer(user.profile,data=request.data,partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
           
            user = get_object_or_404(User.objects.all(),pk=serializer.data['user'])
            user_serializer = UserSerializer(user,many=False)
            return Response(user_serializer.data,status=200)
        else:
            return Response(serializer.errors,status=404)
    
    
    @action(detail=True, methods=['put','get'])
    def followers(self,request,pk=None):
        user = get_object_or_404(User.objects.all(),pk=pk)
        if request.method == 'PUT':
            if request.user in user.profile.follower.all():
                user.profile.follower.remove(request.user)
                return Response(status=204)
            else:
                user.profile.follower.add(request.user)
                return Response(status=200)
        elif request.method == 'GET':
            users = user.profile.follower.all()
            serializer = UserSerializer(users,many=True)
            return Response(serializer.data)




class ProfileApiView(GenericAPIView):
    serializer_class = ProfileSerializer
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    
    def put(self,request):
        serializer = self.serializer_class(data=request.data,instance=request.user.profile,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)

class UpdateAvatarApiView(GenericAPIView):
    serializer_class = UpdateAvatarSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self,request):
        serializer = self.serializer_class(data=request.data,instance=request.user.profile,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)



class UserLoginApiView(GenericAPIView):
    serializer_class = UserLoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            
            refresh = RefreshToken.for_user(user)
            resp = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user':{
                        'id':user.id,
                        'username':user.username
                    }
                }
            return Response(resp,status=200)
        else:
            return Response(serializer.errors,status=404)


class UserRegisterApiView(GenericAPIView):
    serializer_class=UserRegisterSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
        
            resp = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user':{
                        'id':user.id,
                        'username':user.username
                    }
                }
            return Response(resp,status=200)
        else:
            return Response(serializer.errors,status=404)


class UserLogoutApiView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RefreshTokenSerializer
    def post(self,request):
        refresh = request.data.get('refresh')
        if refresh:
            try:
                token = RefreshToken(refresh)
            except:
                return Response(
                    {"detail":"refresh token not valid"},
                    status=403
                )
            token.blacklist()
            return Response({"detail":"successfully logout"},status=200)
        else:
            resp = {
                "refresh":["this field is required"]
            }
            return Response(resp,status=404)


class ChangePasswordApiView(GenericAPIView):
    serializer_class = PassworChangeSerializer

    def put(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            if not check_password(old_password,request.user.password):
                return Response({"old_password":"old password does not match"},status=400)
            request.user.password = serializer.validated_data.get('new_password')
            request.user.save()
            return Response()
        return Response(serializer.errors,status=400)
