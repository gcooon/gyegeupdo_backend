from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """리뷰 시리얼라이저"""
    user_badge = serializers.CharField(source='user.profile.badge', read_only=True, default='none')
    width_score_display = serializers.CharField(source='get_width_score_display', read_only=True)
    size_fit_display = serializers.CharField(source='get_size_fit_display', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'user_badge', 'fit_score', 'width_score', 'width_score_display',
            'size_fit', 'size_fit_display', 'usage_fit', 'pain_level',
            'durability_score', 'comment', 'running_km_at_review', 'created_at'
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    """리뷰 생성 시리얼라이저"""
    class Meta:
        model = Review
        fields = [
            'product', 'fit_score', 'width_score', 'size_fit', 'usage_fit',
            'pain_level', 'durability_score', 'comment', 'running_km_at_review',
            'proof_image_url'
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
