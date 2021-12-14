
from rest_framework import serializers
from ..models.user import User,Profile
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


        
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True,many=False)
    # tutorials = TutorialSerializer(read_only=True,many=True)
    # posts = PostSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields=['id','username','email','last_login','profile','is_superuser','is_active','is_staff']
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


    
