from django.contrib import admin
from .models import Regions, Words, Text, Suffix, News, UsefulLink, Employees


class RegionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)


class WordsAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'created_at')
    search_fields = ('name',)
    list_filter = ('region', 'created_at')


class TextAdmin(admin.ModelAdmin):
    list_display = ('content', 'word', 'created_at')
    search_fields = ('content',)
    list_filter = ('word', 'created_at')


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


# Register models with the admin site
admin.site.register(Regions, RegionsAdmin)
admin.site.register(Words, WordsAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(Suffix, SuffixAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(UsefulLink, UsefulLinkAdmin)
admin.site.register(Employees, EmployeesAdmin)
