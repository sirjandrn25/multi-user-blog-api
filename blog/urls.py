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







urlpatterns = [
    path('',include(router.urls)),
    path("accounts/user_login/",users.UserLoginApiView.as_view()),
    path("accounts/user_logout/",users.UserLogoutApiView.as_view()),
    path("accounts/user_register/",users.UserRegisterApiView.as_view()),
    path("accounts/me/profile/",users.ProfileApiView.as_view()),
    path("accounts/me/update_avatar/",users.UpdateAvatarApiView.as_view()),
    path("accounts/me/change_password/",users.ChangePasswordApiView.as_view()),
    # path("upload-avatar/",UploadAvatarApiView.as_view()),
    path('accounts/user_refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
  

]
