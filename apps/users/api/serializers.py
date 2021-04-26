from rest_framework import serializers
from apps.users.models import User

"""Serializers allow complex data such as querysets and model instances 
    to be converted to native Python datatypes that can then be easily rendered 
    into JSON, XML or other content types.Also provide deserialization.
"""

class UserTokenSerializer(serializers.ModelSerializer):
    """Serializer for user using on apps.users.views
    """
    class Meta:
        model = User
        fields = ('username','email','name','last_name')

class UserSerializer(serializers.ModelSerializer):
    """Serializer for one user
    """
    class Meta:
        model = User
        fields = '__all__'

    def create(self,validated_data):
        #encrypted password
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self,instance,validated_data):
        updated_user = super().update(instance,validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user

class UserListSerializer(serializers.ModelSerializer):
    """Serializer for List all users
    """
    class Meta:
        model = User

    def to_representation(self,instance):
        return {
            'id': instance['id'],
            'username': instance['username'],
            'email': instance['email'],
            'password': instance['password']
        }
