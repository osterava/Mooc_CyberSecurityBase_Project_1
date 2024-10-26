from django.contrib import admin
from .models import Post

@admin.register(Post)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')  
    list_filter = ('author', 'created_at')
