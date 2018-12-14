from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator
from .models import HostProfile,UserHost
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    用户详情序列花类
    """
    access = serializers.SerializerMethodField()
    password = serializers.CharField(
        style={'input_type': 'password'},help_text="密码", label="密码", write_only=True,
    )

    def get_access(self,obj):
        if obj.is_staff:
            return ['admin','other']
        return []

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance,validated_data):
        user = super(UserSerializer, self).update(instance=instance,validated_data=validated_data)
        if 'password' in validated_data.keys():
            user.set_password(validated_data["password"])
            user.save()
        return user

    class Meta:
        model = User
        fields = ("id","username","nickname", "email","is_staff","access","password")


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostProfile
        fields = "__all__"

class UserHostSerializer(serializers.ModelSerializer):
    host = HostSerializer()

    class Meta:
        model = UserHost
        fields = ("host", "id")


class UserHostDetailSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username')
    host_ip = serializers.CharField(source='host.ip')
    def create(self, validated_data):
        validated_data['user'] = User.objects.get(username=validated_data['user']['username'])
        validated_data['host'] = HostProfile.objects.get(ip=validated_data['host']['ip'])
        return super(UserHostDetailSerializer, self).create(validated_data=validated_data)

    class Meta:
        model = UserHost
        validators = [
            UniqueTogetherValidator(
                queryset=UserHost.objects.all(),
                fields=('user', 'host'),
                message="主机已授权"
            )
        ]
        fields = ("user_username", "host_ip","id")

