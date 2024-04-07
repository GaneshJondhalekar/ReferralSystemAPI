from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializers import UserRegistrationSerializer,LoginSerializer
from rest_framework import status
from .models import User
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

#Register api view that accept name,email,password and referral_code(optional) to create user
@api_view(['POST'])
def register_view(request):
    try:
        data=request.data
        serializer=UserRegistrationSerializer(data=data)
        referral_code=request.data.get('referral_code')
        if serializer.is_valid():
            user=serializer.save()
            user.generate_own_referral_code()
            user.referral_code=referral_code
            user.save()
            #if referral_code provided, the user who referred this user will receive a point)
            if referral_code:
                referring_user=User.objects.filter(own_referral_code=referral_code).first()
                referring_user.points+=1
                referring_user.save()
            return Response({
                        'User_ID':serializer.data['id'],
                        'message':"registration successfull"
                    },status=status.HTTP_201_CREATED)

        return Response({
                        'data':serializer.errors,
                        'message':"something wents wrong"
                    },status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            print(e)
            return Response({
                'data':{},
                'message':"something wents wrong"
            },status=status.HTTP_400_BAD_REQUEST)
    
#login view to get access token which will send from authorization header   
@api_view(['POST'])
def login_view(request):
    try:
            data=request.data
            serializer=LoginSerializer(data=data)
            if serializer.is_valid():
                response=serializer.get_jwt_token(serializer.validated_data)
              
                return Response(response,status=status.HTTP_200_OK)
            
            return Response({
                'data':serializer.errors,
                'message':"something wents wrong"
            },status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        print(e)
        return Response({
            'data':{},
            'message':"something wents wrong"
        },status=status.HTTP_400_BAD_REQUEST)
            
