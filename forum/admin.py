from django.contrib import admin
from .models import Category, Subcategory, Thread, Post

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Thread)
admin.site.register(Post)
