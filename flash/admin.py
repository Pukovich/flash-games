from django.contrib import admin
from .models import UserProfile, FlashGame, GameCategory, GameRating, Achievement, UserAchievement

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_points', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['total_points']

@admin.register(GameCategory)
class GameCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(FlashGame)
class FlashGameAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'category', 'views', 'rating']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'author', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['views', 'rating', 'total_ratings']

@admin.register(GameRating)
class GameRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'game__name', 'comment']
    readonly_fields = ['created_at']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'game', 'points', 'created_at']
    list_filter = ['game', 'points']
    search_fields = ['name', 'description', 'game__name']

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'unlocked_at']
    list_filter = ['unlocked_at']
    search_fields = ['user__username', 'achievement__name']
    readonly_fields = ['unlocked_at']
