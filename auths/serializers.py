from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        User = get_user_model()
        model = User
        fields = ['email', 'date_of_birth', 'password', 'repeat_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if (attrs['repeat_password'] != attrs['password']):
            raise serializers.ValidationError(
                {"password": "Passwords do not match."})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('repeat_password')
        # validated_data.pop('is_active')
        # validated_data.pop('is_admin')
        # validated_data.pop('is_superuser')
        # validated_data.pop('groups')
        user = self.Meta.model.objects.create_user(**validated_data)
        return user
