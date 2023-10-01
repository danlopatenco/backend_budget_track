from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the `SubCategory` model.
    """
    name = serializers.ReadOnlyField(source='user.name')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ('name', 'email', 'telegram_user_id', 'bio', 'profile_picture')
