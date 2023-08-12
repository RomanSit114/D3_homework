from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


class PostCategoryInline(admin.TabularInline):
    model = PostCategory

# class PostAdmin(admin.ModelAdmin):
#     inlines = [PostCategoryInline]

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'categoryType', 'get_post_categories', 'dateCreation', 'rating')
    list_filter = ('author', 'categoryType', 'dateCreation', 'rating', 'postCategory__name')
    search_fields = ('title', 'text', 'rating', 'author__authorUser__username', 'categoryType', 'postCategory__name')

    def get_post_categories(self, obj):
        return ", ".join([category.name for category in obj.postCategory.all()])

    get_post_categories.short_description = 'Post Categories'


# class CategoryAdmin(admin.ModelAdmin):
    # filter_horizontal = ('subscribers',)


class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')

# admin.site.register(CustomUser)
# admin.site.register(SubscribedUsers, SubscribedUsersAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor')
    list_filter = ('authorUser', 'ratingAuthor')

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('postThrough', 'categoryThrough')
    list_filter = ('postThrough', 'categoryThrough')
    search_fields = ('postThrough__title', 'categoryThrough__name')

admin.site.register(Author, AuthorAdmin)
# admin.site.register(Category, CategoryAdmin)
admin.site.register(Category)
# admin.site.register(Post)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment)
# admin.site.register(SubscribedUsers)



