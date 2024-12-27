from rest_framework import serializers
from .models import Text, Suffix, News, UsefulLink, Employees, Regions, Contact, Publications, \
    About, CategoryProject, AboutProject


# News

class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'created_at']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'text', 'created_at']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


# UsefulLink

class UsefulLinkSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    class Meta:
        model = UsefulLink
        fields = ['id', 'image', 'title', 'last_title', 'text', 'created_at', 'link']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_text(self, obj):
        # Faqat 100 ta belgi oling, ortidan "..." qo'shiladi agar uzunroq bo'lsa
        if obj.text:
            return obj.text[:100] + "..." if len(obj.text) > 100 else obj.text
        return None


class UsefulLinkLatestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsefulLink
        fields = ['id', 'title', 'image', 'link']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


# Employees

class EmployeesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ['id', 'full_name', 'image', 'degree', 'position', 'order']


# Region Statistic

class RegionStatisticsSerializer(serializers.ModelSerializer):
    word_count = serializers.IntegerField()

    class Meta:
        model = Regions
        fields = ['id', 'name', 'word_count']


# Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'full_name', 'phone', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


# Publications


class PublicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publications
        fields = ['id', 'title', 'image', 'file']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


# Text

class TextDetailSerializer(serializers.ModelSerializer):
    word_name = serializers.SerializerMethodField()

    class Meta:
        model = Text
        fields = ['id', 'source', 'content', 'word_name', 'created_at']

    def get_word_name(self, obj):
        if obj.word:
            return obj.word.name  # `Words` modelidagi `name` maydoni
        return None  # Agar `word` bo'sh bo'lsa, `None` qaytariladi


# About
class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['id', 'phone', 'email', 'location_name', 'location_link']


# About Project

class AboutProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutProject
        fields = ['id', 'tasnif']  # `AboutProject`ning kerakli maydonlari


class CategoryProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProject
        fields = ['id', 'name']  # `CategoryProject` modelining maydonlari


class CategoryProjectDetailSerializer(serializers.ModelSerializer):
    # `CategoryProject`ga tegishli `AboutProject`larni ko'rsatamiz
    loyhalar = AboutProjectSerializer(many=True, read_only=True)

    class Meta:
        model = CategoryProject
        fields = ['id', 'name', 'loyhalar']  # `CategoryProject` modelining maydonlari
