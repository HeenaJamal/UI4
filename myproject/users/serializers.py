from rest_framework import serializers
from .models import User, UploadedFile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'mobile', 'otp']

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['table_name', 'file']
