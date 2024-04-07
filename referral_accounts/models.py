from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
import uuid

#custom user manage  to create user and super_user
class CustomManager(BaseUserManager):
    def create_user(self,email,password=None,**extra):
        if email is None:
            raise ValueError("Email is Required")
        email=self.normalize_email(email)
        user=self.model(email=email,**extra)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password=None,**extra):
        extra.setdefault("is_staff",True)
        extra.setdefault("is_superuser",True)
        extra.setdefault("is_active",True)
        return self.create_user(email,password,**extra)
        
#Custom User model
class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.EmailField(unique=True)
    name=models.CharField(max_length=20)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    referral_code = models.CharField(max_length=8, blank=True, null=True)
    own_referral_code = models.CharField(max_length=8, blank=True, null=True)
    timestamp_of_registration = models.DateTimeField(auto_now_add=True)
    points=models.IntegerField(default=0)
    objects=CustomManager()

    USERNAME_FIELD='email' #used email as username field for login perpose
    REQUIRED_FIELDS=["name"]

    def __str__(self):
        return self.name
    
    def generate_own_referral_code(self):
        if not self.own_referral_code:
            self.own_referral_code = str(uuid.uuid4())[:8] 
            self.save()