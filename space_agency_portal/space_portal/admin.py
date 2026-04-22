from django.contrib import admin
from .models import Mission, Astronaut, Launch, NewsArticle, SpacecraftGallery, ContactMessage, UserProfile


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'mission_type', 'status', 'launch_date', 'agency']
    list_filter = ['status', 'mission_type']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Astronaut)
class AstronautAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'status', 'missions_count', 'hours_in_space']
    list_filter = ['status', 'nationality']
    search_fields = ['name', 'nationality']
    filter_horizontal = ['missions']


@admin.register(Launch)
class LaunchAdmin(admin.ModelAdmin):
    list_display = ['rocket_name', 'mission', 'launch_site', 'launch_datetime', 'status']
    list_filter = ['status']


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'published_at', 'is_featured']
    list_filter = ['category', 'is_featured']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(SpacecraftGallery)
class SpacecraftGalleryAdmin(admin.ModelAdmin):
    list_display = ['name', 'spacecraft_type', 'manufacturer', 'first_flight']
    search_fields = ['name', 'manufacturer']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'submitted_at', 'is_read']
    list_filter = ['is_read']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']
