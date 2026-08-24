from django.contrib import admin
from app.models import Article, UserProfile
from django.contrib.auth.admin import UserAdmin


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "word_count", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("title", "content")
    date_hierarchy = "created_at"
    ordering = ("created_at",)
    readonly_fields = ("word_count", "created_at", "updated_at")


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),

    )
    list_display = ("username", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)


admin.site.register(Article, ArticleAdmin)
admin.site.register(UserProfile, CustomUserAdmin)
