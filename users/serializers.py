from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """회원가입 시리얼라이저"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    nickname = serializers.CharField(required=True, max_length=50)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'nickname']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],  # username으로 email 사용
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['nickname'],
        )
        # 프로필 자동 생성
        UserProfile.objects.create(user=user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """사용자 프로필 시리얼라이저"""
    badge_display = serializers.CharField(source='get_badge_display', read_only=True)
    foot_width_display = serializers.CharField(source='get_foot_width_display', read_only=True)
    pronation_display = serializers.CharField(source='get_pronation_display', read_only=True)
    usage_type_display = serializers.CharField(source='get_usage_type_display', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'foot_width', 'foot_width_display', 'pronation', 'pronation_display',
            'usage_type', 'usage_type_display', 'budget_min', 'budget_max',
            'priority', 'total_km', 'badge', 'badge_display', 'review_weight',
            'review_count', 'dispute_accepted_count', 'created_at'
        ]


class UserSerializer(serializers.ModelSerializer):
    """사용자 시리얼라이저"""
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'profile']


class BadgeProgressSerializer(serializers.Serializer):
    """배지 진행률 시리얼라이저"""
    current_badge = serializers.CharField()
    next_badge = serializers.CharField()
    progress = serializers.DictField()
