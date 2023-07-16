from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


class PostCategoryInline(admin.TabularInline):
    model = PostCategory

class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInline]

class CategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('subscribers',)

admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Post)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)


