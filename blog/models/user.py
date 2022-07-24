
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators


class UserManager(BaseUserManager):
    use_in_migrations = True

    # Method to save user to the database
    def save_user(self, username, password,email=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        if email:
            email = self.normalize_email(email)
        user = self.model(email=email,username=username, **extra_fields)

        # Call this method for password hashing
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,username, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self.save_user(username, password, **extra_fields)

    # Method called while creating a staff user
    def create_staffuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = False
        
        return self.save_user(email, password, **extra_fields) 

    # Method called while calling creatsuperuser
    def create_superuser(self,username, password, email=None,**extra_fields):

        # Set is_superuser parameter to true
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser should be True')
        
        extra_fields['is_staff'] = True

        return self.save_user(username,email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    gender_choices = [
        ('male','Male'),
        ('female','Female')
    ]
    # Primary key of the model
    id = models.BigAutoField(
        primary_key = True,
    )

    username=models.CharField(max_length=100,unique=True)
    # Email field that serves as the username field
    email = models.CharField(
        max_length = 100, 
        unique = True,
        validators = [validators.EmailValidator()],
        verbose_name = "Email",
        blank=True,
        null=True
    )

    # Other required fields for authentication
    # If the user is a staff, defaults to false
    is_staff = models.BooleanField(default=False)

    # If the user account is active or not. Defaults to True.
    # If the value is set to false, user will not be allowed to sign in.
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'
    
    # Custom user manager
    objects = UserManager()
    def __str__(self):
        return self.username





class Profile(models.Model):
    gender_choices = (
        ("male","male"),
        ("female","female"),
        ("other","other")
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=10)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    avatar = models.ImageField(upload_to="avatar/",null=True,blank=True)
    # avatar = models.CharField(max_length=400,blank=True,null=True)
    address = models.CharField(max_length=150,blank=True)
    birth_date = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=10,choices=gender_choices,default=gender_choices[0][1])
    follower = models.ManyToManyField(User,blank=True,related_name="followers")
    description = models.CharField(max_length=300,blank=True)

    def __str__(self):
        return self.user.username

class Social(models.Model):
    facebook = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username