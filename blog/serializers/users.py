
from blog.models.post import Post
from rest_framework import serializers
from ..models.user import Social, User,Profile
from django.contrib.auth.hashers import check_password,make_password
from django.db.models import Q




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','contact_no','avatar','address','gender','birth_date','follower']
        read_only_fields = ['avatar','follower']
    
    def validate(self,validated_data):

        contact_no = validated_data.get('contact_no')
        if not contact_no.isdigit():
            errors = {
                'contact_no':['only numeric values are allowed']
            }
        elif len(contact_no) !=10:
            errors = {
                'contact_no':['10 digits are required']
            }
        else:
            return validated_data
        
        raise serializers.ValidationError(errors)
            
class UpdateAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']


def get_postSerializer(post):
    thumbnail = ''
    if post.thumbnail:
        thumbnail = post.thumbnail.url
    
    data = {
        'id':post.id,
        'title':post.title,
        'description':post.description,
        'thumbnail':thumbnail,
        'created_at':post.created_at
        
    }
    return data
    
        
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True,many=False)
    posts = serializers.SerializerMethodField()
    social = serializers.SerializerMethodField()
    def get_posts(self,obj):
        posts = Post.objects.filter(user=obj)[:5]
        
        data = {
            'total_posts':len(posts),
            'recent_posts': [get_postSerializer(post) for post in posts]
            
        }
        return data
    
    def get_social(self,obj):
        social = Social.objects.filter(user=obj).first()
        if social:
            return {
                'facebook':social.facebook,
                'twitter':social.twitter,
                'instagram':social.instagram
            }
        return social
    
    class Meta:
        model = User
        fields=['id','username','email','last_login','profile','is_superuser','is_active','is_staff','social','posts']
        read_only_fields = ['id','password','username','posts','social']
        
  

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,validated_data):
        
        username = validated_data.get('username','')
        password = validated_data.get('password','')
       
        if username and password:
            try:
                user = User.objects.get(Q(username=username) | Q(email=username))
            except Exception as e:
                print(e)
                errors = {
                    'username':['this username is does not exist']
                }
                raise serializers.ValidationError(errors)
            if check_password(password,user.password):
                validated_data['user']=user
                return validated_data
            else:
                errors = {
                    'password':['password is does not matched']
                }
                raise serializers.ValidationError(errors)
            
        else:
            errors = {
                'username':["this field is required"],
                'password':['this field is required']
            }
            raise serializers.ValidationError(errors)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']

    def validate(self,validated_data):
        password = validated_data.get('password')
        if password.isdigit():
            errors = {
                'password':["only numeric values are not allowed"]
            }
        elif len(password)<8:
            errors = {
                'password':["atleast 8 charecters are required"]
            }
        else:
            validated_data['password'] = make_password(password)
            return validated_data
        raise serializers.ValidationError(errors)

class PassworChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate(self,validated_data):
        new_password = validated_data.get('old_password')
        if new_password.isdigit():
            errors = {
                "old_password":["only numeric values not allowed"]
            }
        else:
            validated_data['new_password'] = make_password(new_password)
            return validated_data


    


class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self,validated_data):
        email = validated_data.get('email')
        if User.objects.filter(email=email).first():
            return validated_data
        errors = {
            'email':[f'this email does not exist']
        }
        raise serializers.ValidationError(errors)

class UsernameVerifySerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self,validated_data):
        username = validated_data.get('username')
        print(User.objects.filter(username=username).first())
        if User.objects.filter(username=username).first():
            return validated_data
        errors = {
            'username':[f'this username does not exist']
        }
        raise serializers.ValidationError(errors)

class UsernameOrEmailVerifySerializer(serializers.Serializer):
    email_or_username = serializers.CharField()

    

    def validate(self,validated_data):
        email_or_username = validated_data.get('email_or_username')

        if User.objects.filter(Q(username = email_or_username) | Q(email=email_or_username)).first():
            return validated_data
        raise serializers.ValidationError({'email_or_username':['email or username does not exists']})
    
