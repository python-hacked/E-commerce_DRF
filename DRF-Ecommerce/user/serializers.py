
from .models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django_countries.serializer_fields import CountryField


class UserSerializer(serializers.ModelSerializer):
    """ UserSerializer model class """
    confirm_password = serializers.CharField(style={'input_type': 'password'}, max_length=70,
                                             min_length=5, write_only=True)

    class Meta:
        """ User serializer Meta class """
        model = User
        fields = ['id', 'name', 'email', 'password', 'confirm_password', 'gender', 'contact',
                  'date_of_birth', 'city', 'state', 'address', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """ Create and return a new `User` instance, given the validated data."""
        validated_data.pop('confirm_password', None)
        user = super(UserSerializer, self).create(validated_data)
        user.password = make_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Those password don't match")
        return attrs

    def update(self, instance, validated_data):
        """ Update user's instance"""
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance



