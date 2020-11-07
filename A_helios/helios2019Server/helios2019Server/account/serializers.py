from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserRegisterSerializer(serializers.ModelSerializer):
    """
      User注册时的序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'groups')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        attrs['password'] = make_password(attrs['password'])
        return attrs


class UserLoginSerializer(serializers.ModelSerializer):
    """
      User登录时的序列化器
    """
    token = serializers.CharField(
        label='登录状态token', read_only=True)  # 增加token字段

    class Meta:
        model = User
        fields = ('id', 'username', 'token', 'password', 'groups')
        extra_kwargs = {'password': {'write_only': True},
                        'groups': {'read_only': True}}

    def validate(self, attrs):
        user_obj = User.objects.filter(username=attrs['username']).first()
        if user_obj:
            if check_password(attrs['password'], user_obj.password):
                return attrs
        raise ValidationError('用户名或密码错误')
