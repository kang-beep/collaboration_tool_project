from rest_framework import serializers
from .models import CustomUser,FriendRequest

class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password2', 'email', 'name', 'contact', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}  # 비밀번호 필드를 쓰기 전용으로 설정

    def create(self, validated_data):
        validated_data.pop('password2', None)  # password2 필드를 validated_data에서 제외
        return super().create(validated_data)


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = CustomUserSerializer(read_only=True)
    to_user = serializers.SlugRelatedField(slug_field='username', queryset = CustomUser.objects.all())
    
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'timestamp', 'accepted']
        read_only_fields = ['id', 'from_user', 'timestamp', 'accepted']
