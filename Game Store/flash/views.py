from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import UserProfile, FlashGame, GameCategory, GameRating, Achievement, UserAchievement
from .forms import (
    UserRegistrationForm, UserLoginForm, UserProfileForm, UserUpdateForm,
    GameRatingForm
)
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Avg, Q
from django.core.paginator import Paginator
from django.http import JsonResponse

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Аккаунт успешно создан! Теперь вы можете войти.')
            return redirect('flash:login')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'flash/auth/register.html', context)

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('flash:store')
    else:
        form = UserLoginForm()
    return render(request, 'flash/auth/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы!')
    return redirect('flash:store')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('flash:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'flash/profile.html', context)

@login_required
def store(request):
    games = FlashGame.objects.all()
    categories = GameCategory.objects.all()
    
    # Фильтрация по категории
    category_slug = request.GET.get('category')
    if category_slug:
        games = games.filter(category__slug=category_slug)
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        games = games.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(author__icontains=search_query)
        )
    
    # Сортировка
    sort = request.GET.get('sort', '-created_at')
    if sort == 'rating':
        games = games.order_by('-rating', '-total_ratings')
    elif sort == 'views':
        games = games.order_by('-views')
    elif sort == 'name':
        games = games.order_by('name')
    else:
        games = games.order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(games, 12)
    page = request.GET.get('page')
    games = paginator.get_page(page)
    
    context = {
        'games': games,
        'categories': categories,
        'current_category': category_slug,
        'current_sort': sort,
        'search_query': search_query,
    }
    return render(request, 'flash/games/list.html', context)

def play_game(request, game_slug):
    game = get_object_or_404(FlashGame, slug=game_slug)
    game.increment_views()
    
    # Получаем рейтинг пользователя, если он авторизован
    user_rating = None
    if request.user.is_authenticated:
        user_rating = GameRating.objects.filter(user=request.user, game=game).first()
    
    # Получаем все рейтинги игры
    ratings = GameRating.objects.filter(game=game).select_related('user').order_by('-created_at')
    
    # Получаем достижения игры
    achievements = Achievement.objects.filter(game=game)
    
    # Если пользователь авторизован, получаем его достижения
    user_achievements = None
    if request.user.is_authenticated:
        user_achievements = UserAchievement.objects.filter(
            user=request.user,
            achievement__in=achievements
        ).select_related('achievement')
    
    if request.method == 'POST' and request.user.is_authenticated:
        rating_form = GameRatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user
            rating.game = game
            rating.save()
            messages.success(request, 'Ваша оценка успешно добавлена!')
            return redirect('flash:play_game', game_slug=game.slug)
    else:
        rating_form = GameRatingForm()
    
    context = {
        'game': game,
        'user_rating': user_rating,
        'ratings': ratings,
        'rating_form': rating_form,
        'achievements': achievements,
        'user_achievements': user_achievements,
    }
    return render(request, 'flash/games/play.html', context)

def play_game_by_id(request, game_id):
    game = get_object_or_404(FlashGame, id=game_id)
    return redirect('flash:play_game', game_slug=game.slug)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('flash:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'flash/auth/profile.html', {
        'form': form,
        'title': 'Изменение пароля'
    })

@login_required
def unlock_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, id=achievement_id)
    user = request.user
    
    # Проверяем, не получено ли уже достижение
    if UserAchievement.objects.filter(user=user, achievement=achievement).exists():
        return JsonResponse({'status': 'error', 'message': 'Достижение уже получено'})
    
    # Создаем запись о получении достижения
    UserAchievement.objects.create(user=user, achievement=achievement)
    
    # Обновляем очки пользователя
    user.profile.update_points()
    
    return JsonResponse({
        'status': 'success',
        'message': f'Достижение "{achievement.name}" получено!',
        'points': achievement.points
    })
