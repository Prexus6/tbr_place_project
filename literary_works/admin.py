from django.contrib import admin
from tinymce.widgets import TinyMCE
from .models import LiteraryWork, Category
from django.db import models


@admin.register(LiteraryWork)
class LiteraryWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'published', 'created_at')
    list_filter = ('category', 'published')
    search_fields = ('title', 'description', 'content')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
