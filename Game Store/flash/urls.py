from django.urls import path
from . import views

app_name = 'flash'

urlpatterns = [
    # Основные страницы
    path('', views.store, name='store'),
    path('game/id/<int:game_id>/', views.play_game_by_id, name='play_game_by_id'),
    path('game/<int:game_id>/', views.play_game_by_id, name='play_game_by_id'),
    path('game/<slug:game_slug>/', views.play_game, name='play_game'),

    # Аутентификация
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Профиль
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('achievement/<int:achievement_id>/unlock/', views.unlock_achievement, name='unlock_achievement'),
]