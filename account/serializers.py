from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'avatar', 'phone', 'about_me', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=8, max_length=20,
                                      required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2',
                  'first_name', 'last_name', 'username', 'phone')

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs.pop('password2')
        if password2 != password:
            raise serializers.ValidationError('Passwords didn\'t match!')
        validate_password(password)
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'avatar',
                  'about_me', 'account_type', 'subscription_type', 'subscription_start')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['is_superuser'] = self.user.is_superuser
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
