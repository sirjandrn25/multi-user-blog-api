
from rest_framework import serializers
from ..models.user import User,Profile
from django.contrib.auth.hashers import check_password,make_password
from django.db.models import Q



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','contact_no','address','gender','birth_date']
    
    def validate(self,validated_data):

        contact_no = validated_data.get('contact_no')
        if not contact_no.isdigit():
            errors = {
                'contact_no':['only numeric values are allowed']
            }
        elif len(contact_no)==10:
            errrors = {
                'contact_no':['10 digits are required']
            }
        else:
            return validated_data
        
        raise serializers.ValidationError(errors)
            
class UpdateAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']
        

        
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True,many=False)
    # tutorials = TutorialSerializer(read_only=True,many=True)
    # posts = PostSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields=['id','username','email','last_login','profile']
        read_only_fields = ['id','password','username']
        ordering = ['id']
  

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


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    re_password = serializers.CharField()

    def validate(self,validated_data):
        username = validated_data.get('username','')
        email = validated_data.get('email','')
        password = validated_data.get('password','')
        re_password = validated_data.get('re_password','')

        if username and password and email and re_password:
            if User.objects.filter(username=username).first() is None:
                if password != re_password:
                    errors = {
                        're_password':["both password is not matched"]
                    }
                elif password.isdigit():
                    errors = {
                        'password':['only numeric values are not allowed']
                    }
                elif len(password)<8:
                    errors = {
                        'password':['at least 8 charecters are required']
                    }
                else:
                    user = User(username=username,email=email,password=make_password(password))
                    user.save()
                    validated_data['user'] = user
                    return validated_data
            else:
                errors = {
                    'username':['this username is alredy exist']
                }
                
        else:
            errors = {
                'username':['this field is required'],
                'email':['this field is required'],
                'password':['this field is required'],
                're_password':['this field is required']
            }
        raise serializers.ValidationError(errors)