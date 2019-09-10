from rest_framework import serializers

from .models import News

class NewsSerializer(serializers.ModelSerializer):
    """News serializer"""
    class Meta:
        model = News
        fields = '__all__'
