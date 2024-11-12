import boto3
from botocore.exceptions import ClientError
import jwt
import os
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

def verify_access_token(access_token):
    # Initialize a session using Amazon DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

    # Select your DynamoDB table
    table = dynamodb.Table('CSV_converter_users')
    try:
        # Decode the JWT token to get the username
        decoded_token = AccessToken(access_token).payload

        if not decoded_token:
            return False
        
        if 'exp' in decoded_token:
            if datetime.utcfromtimestamp(decoded_token['exp']) < datetime.utcnow():
                return False
        
        if 'username' not in decoded_token:
            return False
       
        username = decoded_token.get('username')

        # Query the DynamoDB table to verify the username
        response = table.get_item(Key={'username': username})

        if 'Item' in response:
            # Username found in the table
            return True
        else:
            # Username not found in the table
            return False

    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return False
    except jwt.InvalidTokenError:
        print("Invalid token")
        return False