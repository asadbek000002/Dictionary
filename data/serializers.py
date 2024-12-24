from rest_framework import serializers
from .models import Text, Suffix, News, UsefulLink, Employees, Regions


# News

class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'created_at']


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'text', 'created_at']


# UsefulLink

class UsefulLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsefulLink
        fields = ['id', 'title', 'image', 'link']


class UsefulLinkDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsefulLink
        fields = ['id', 'title', 'image', 'text', 'link']

# Employees

class EmployeesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ['id', 'full_name', 'image', 'info_text', 'degree', 'position', 'order']


# Region Statistic

class RegionStatisticsSerializer(serializers.ModelSerializer):
    word_count = serializers.IntegerField()

    class Meta:
        model = Regions
        fields = ['id', 'name', 'word_count']