
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email','referral_code','timestamp_of_registration','password']


    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']

        )
        return user
    

class LoginSerializer(serializers.Serializer):
    email=serializers.CharField()
    password=serializers.CharField()

   
    def get_jwt_token(self,data):
        print("Hi>>>>>>>")
        user=authenticate(username=data['email'],password=data['password'])
      
        if user is None:
            return {'data':{},'message':"Invalid credentials"}
        
        refresh=RefreshToken.for_user(user)
        access=refresh.access_token
        print(user,"Hi>>>>>>>")
        return {'data':{'token':{'access':str(access),'refresh':str(refresh)}},'message':'Login succesfull'}



#user detals serializer to show data like name, email, referral_code, timestamp of registration
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email','referral_code','timestamp_of_registration']


class MyReferralsSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','timestamp_of_registration']