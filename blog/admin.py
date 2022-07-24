from django.contrib import admin

from django.utils.html import format_html
from django.contrib.admin import AdminSite
from .models.user import User

from django.contrib.auth.admin import UserAdmin
from .models import *
from django_quill.fields import QuillField


admin.site.register(User)
admin.AdminSite.site_header=format_html("<h3>Learn More</h3>")

class MyAdminSite(AdminSite):
    site_title = "Admin Login"

admin_site = MyAdminSite()




# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ['likes']
    list_display = ['title','user','category','total_likes','views','created_at']
    date_hierarchy = 'created_at'

    list_filter = [
        'category',
        
    ]
    search_fields = ['title','user__username']
    body = QuillField()
    @admin.display
    def total_likes(self,obj):
        return len(obj.likes.all())
   
    

    
class ProfileInline(admin.StackedInline):
    model = Profile


    



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','user','content','post','created_at']
    search_fields = ['user__username','post__title']
    date_hierarchy = 'created_at'

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    
    list_display = ['id','user','content','comments','created_at','post']
    search_fields = ['user__username','content']
    date_hierarchy = "created_at"

    @admin.display
    def comments(self,obj):
        return obj.comment.content
    
    @admin.display
    def post(self,obj):
        return obj.comment.post.title

admin.site.register(Category)
# admin.site.register(Profile)
# admin.site.register(Comment)
# admin.site.register(Reply)
admin.site.register(Tutorial)
admin.site.register(Profile)
admin.site.register(Social)
