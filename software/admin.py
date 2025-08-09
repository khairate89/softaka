from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
import nested_admin
from .models import (
    NewsletterSubscriber, Category, Software, SoftwareVersion, DownloadLink,
    SoftwareDownloadPageVersion, DownloadPageSpecificLink, Comment
)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'timestamp')  # Fields to display in the list view
    search_fields = ('email',)             # Allow searching by email
    list_filter = ('timestamp',)           # Allow filtering by date
    ordering = ('-timestamp',)             # Default ordering for the list

# CATEGORY ADMIN
@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'icon', 'display_on_menu', 'display_on_header')
    prepopulated_fields = {'slug': ('name',)}

# NESTED INLINE: DownloadLink under SoftwareVersion
class DownloadLinkInline(nested_admin.NestedTabularInline):
    model = DownloadLink
    extra = 1
    fields = ['name', 'url', 'order']

# NEW: Register the Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'software', 'created_at', 'approved_comment')
    list_filter = ('approved_comment', 'created_at')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved_comment=True)
        self.message_user(request, "Selected comments have been successfully approved.")
    approve_comments.short_description = "Approve selected comments"

# INLINE: SoftwareVersion with DownloadLink as nested
class SoftwareVersionInline(nested_admin.NestedTabularInline):
    model = SoftwareVersion
    extra = 1
    fields = ['version_number', 'release_date', 'download_link_url', 'is_current_version']
    inlines = [DownloadLinkInline]

# NESTED INLINE: DownloadPageSpecificLink under SoftwareDownloadPageVersion
class DownloadPageSpecificLinkInline(nested_admin.NestedTabularInline):
    model = DownloadPageSpecificLink
    extra = 1
    fields = ['name', 'url', 'file_size', 'order']

# INLINE: SoftwareDownloadPageVersion with its own nested DownloadPageSpecificLink
class SoftwareDownloadPageVersionInline(nested_admin.NestedTabularInline):
    model = SoftwareDownloadPageVersion
    extra = 1
    fields = ['version_number', 'display_title', 'release_date']
    inlines = [DownloadPageSpecificLinkInline]

# SOFTWARE ADMIN (Main Admin) — note TranslationAdmin first
@admin.register(Software)
class SoftwareAdmin(TranslationAdmin, nested_admin.NestedModelAdmin):
    list_display = ('name', 'category', 'operating_system', 'get_current_version', 'created_at', 'updated_at')
    list_filter = ('category', 'operating_system', 'license_type')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'operating_system', 'license_type', 'file_size', 'website_link', 'image')
        }),
        ('Content', {
            'fields': ('description', 'homepage_description', 'requirements')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
    inlines = [SoftwareVersionInline, SoftwareDownloadPageVersionInline]

    def get_current_version(self, obj):
        current_version = obj.versions.filter(is_current_version=True).first()
        if current_version:
            if current_version.release_date:
                return f"v{current_version.version_number} ({current_version.release_date.strftime('%Y-%m-%d')})"
            else:
                return f"v{current_version.version_number}"
        return "N/A"
    get_current_version.short_description = 'Current Version'

# NEW: Register SoftwareDownloadPageVersion and define its admin options
@admin.register(SoftwareDownloadPageVersion)
class SoftwareDownloadPageVersionAdmin(nested_admin.NestedModelAdmin):
    list_display = ('id', 'software', 'version_number', 'display_title', 'release_date')
    inlines = [DownloadPageSpecificLinkInline]
    search_fields = ('version_number', 'display_title')
    list_filter = ('software', 'release_date')
