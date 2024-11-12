from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .serializers import UserLoginSerializer
from . models import User
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.permissions import AllowAny
import boto3
import uuid

dynamo_db_client=boto3.resource('dynamodb', region_name='us-east-2')

class LoginView(CreateAPIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        table=dynamo_db_client.Table('CSV_converter_users')
        key = {
            'username': request.data['username']
        }
        response = table.get_item(Key=key)
        if 'Item' not in response:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        user_data=response.get('Item')
        if not check_password(request.data['password'], user_data['password']):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        class User:
            def __init__(self, username):
                self.id=uuid.uuid4()
                self.username = username
        refresh = RefreshToken.for_user(User(user_data['username']))
        access = AccessToken.for_user(User(user_data['username']))
        access['username'] = user_data['username']
        refresh['username'] = user_data['username']
        return Response({
            'access_token': f'Bearer {str(access)}',
            'refresh_token': f'Bearer {str(refresh)}'
        }, status=status.HTTP_200_OK)

# class SignUPview(CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         user_item={
            # 'id':str(uuid.uuid4()),
#             'username':request.data['username'],
#             'password':make_password(request.data['password']),
#             'email':request.data['email'],
#             'name':request.data['name']
#         }
#         table=dynamo_db_client.Table('CSV_converter_users')
#         table.put_item(Item=user_item)
#         return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)