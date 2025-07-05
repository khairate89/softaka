from django.contrib import admin
import nested_admin

from .models import (
    Category, Software, SoftwareVersion, DownloadLink,
    SoftwareDownloadPageVersion, DownloadPageSpecificLink, Comment # NEW: Import Comment
)

# CATEGORY ADMIN
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
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
    actions = ['approve_comments'] # Add a custom action

    def approve_comments(self, request, queryset):
        queryset.update(approved_comment=True)
        self.message_user(request, "Selected comments have been successfully approved.")
    approve_comments.short_description = "Approve selected comments"

# INLINE: SoftwareVersion with DownloadLink as nested
class SoftwareVersionInline(nested_admin.NestedTabularInline):
    model = SoftwareVersion
    extra = 1
    fields = ['version_number', 'release_date', 'download_link_url', 'is_current_version', 'additional_info']
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
    fields = ['version_number', 'display_title', 'release_date', 'additional_info']
    inlines = [DownloadPageSpecificLinkInline]


# SOFTWARE ADMIN (Main Admin)
@admin.register(Software)
class SoftwareAdmin(nested_admin.NestedModelAdmin):
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
            return f"v{current_version.version_number} ({current_version.release_date.strftime('%Y-%m-%d')})" if current_version.release_date else f"v{current_version.version_number}"
        return "N/A"
    get_current_version.short_description = 'Current Version'
# NEW: Register SoftwareDownloadPageVersion and define its admin options
@admin.register(SoftwareDownloadPageVersion)
class SoftwareDownloadPageVersionAdmin(nested_admin.NestedModelAdmin):
    list_display = ('id', 'software', 'version_number', 'display_title', 'release_date')
    inlines = [DownloadPageSpecificLinkInline] # If you want to manage nested links here
    search_fields = ('version_number', 'display_title')
    list_filter = ('software', 'release_date')