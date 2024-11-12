from rest_framework.serializers import ModelSerializer
from .models import User

class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
