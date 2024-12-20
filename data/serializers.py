from rest_framework import serializers
from .models import Text, Suffix, News, UsefulLink


class TextSearchResultSerializer(serializers.Serializer):
    word = serializers.CharField()
    start_idx = serializers.IntegerField()
    end_idx = serializers.IntegerField()


class TextSerializer(serializers.ModelSerializer):
    matches = TextSearchResultSerializer(many=True)

    class Meta:
        model = Text
        fields = ['id', 'content', 'matches']


class SuffixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suffix
        fields = ['suffix', 'description']


# News

class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'created_at']


# Havola

class UsefulLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsefulLink
        fields = ['id', 'title', 'image', 'link']
