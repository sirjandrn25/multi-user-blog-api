from django.urls import path,include
from rest_framework import routers

from blog.views import tutorials
from .views import posts, users,comments_replies


router = routers.SimpleRouter()
router.register('posts',posts.PostApiView,basename="post")
router.register('categories',posts.CategoryApiView,basename="category")
router.register('users',users.UserApiView,basename="user")
router.register('comments',comments_replies.CommentApiView,basename="comment")
router.register('replies',comments_replies.ReplyApiView,basename="reply")
router.register('tutorials',tutorials.TutorialApiView,basename="tutorial")
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('',include(router.urls)),
    path("authentication/user_login/",users.UserLoginApiView.as_view()),
    path("authentication/user_logout/",users.UserLogoutApiView.as_view()),
    path("authentication/user_register/",users.UserRegisterApiView.as_view()),
    # path("upload-avatar/",UploadAvatarApiView.as_view()),
    path('authentication/user_refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),

    path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
  

]
