from django.contrib import admin
from .models import Regions, Words, Text, Suffix, News, UsefulLink, Employees, SearchHistory, Contact, Publications


class RegionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)


class WordsAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'created_at')
    search_fields = ('name',)
    list_filter = ('region', 'created_at')


class TextAdmin(admin.ModelAdmin):
    list_display = ('short_content', 'word', 'created_at')
    search_fields = ('content',)
    list_filter = ('word', 'created_at')

    def short_content(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')

    short_content.short_description = 'Content'


class SuffixAdmin(admin.ModelAdmin):
    list_display = ('suffix', 'description', 'created_at')
    search_fields = ('suffix',)
    list_filter = ('created_at',)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'text')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


class UsefulLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'created_at')
    search_fields = ('title', 'text', 'link')
    list_filter = ('created_at',)


class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'degree', 'position', 'created_at')
    search_fields = ('full_name', 'degree', 'position')
    list_filter = ('created_at',)


class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('get_word_name', 'count', 'created_at')
    search_fields = ('word__name', 'missing_word')
    list_filter = ('created_at',)

    def get_word_name(self, obj):
        if obj.word:
            return obj.word.name  # Agar 'word' mavjud bo'lsa, uning nomini qaytarish
        return obj.missing_word  # Agar 'word' bo'lmasa, 'missing_word'ni qaytarish

    get_word_name.admin_order_field = 'word__name'  # Sort qilish uchun 'word' nomi bo'yicha
    get_word_name.short_description = 'Word/Missing Word'  # Admin panelda chiqadigan nom


class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'created_at')
    search_fields = ('full_name', 'phone',)
    list_filter = ('created_at',)


class PublicationsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)

# Register models with the admin site
admin.site.register(Regions, RegionsAdmin)
admin.site.register(Words, WordsAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(Suffix, SuffixAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(UsefulLink, UsefulLinkAdmin)
admin.site.register(Employees, EmployeesAdmin)
admin.site.register(SearchHistory, SearchHistoryAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Publications, PublicationsAdmin)
