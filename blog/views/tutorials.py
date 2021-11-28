from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..serializers import TutorialSerializer
from ..models.post import Tutorial
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsOwnUserOrIsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .paginations import MyPageNumberPagination
from django.shortcuts import get_object_or_404



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