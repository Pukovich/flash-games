from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
import os

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name='Аватар'
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)]
    )
    total_points = models.IntegerField(default=0, verbose_name='Всего очков')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"{self.user.username}'s profile"

    def add_balance(self, amount):
        """Добавить средства на баланс"""
        if amount > 0:
            self.balance += amount
            self.save()
            return True
        return False

    def subtract_balance(self, amount):
        """Списать средства с баланса"""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

    def update_points(self):
        self.total_points = sum(ua.achievement.points for ua in self.user.achievements.all())
        self.save(update_fields=['total_points'])

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class GameCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Категория игр'
        verbose_name_plural = 'Категории игр'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

def validate_swf_file(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.swf':
        raise ValidationError('Поддерживаются только SWF файлы.')

class Achievement(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    icon = models.ImageField(upload_to='achievements/', verbose_name='Иконка')
    points = models.IntegerField(default=10, verbose_name='Очки')
    game = models.ForeignKey('FlashGame', on_delete=models.CASCADE, related_name='achievements', verbose_name='Игра')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'
        ordering = ['-points']

    def __str__(self):
        return f"{self.name} - {self.game.name}"

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements', verbose_name='Пользователь')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='users', verbose_name='Достижение')
    unlocked_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения')

    class Meta:
        verbose_name = 'Достижение пользователя'
        verbose_name_plural = 'Достижения пользователей'
        unique_together = ['user', 'achievement']
        ordering = ['-unlocked_at']

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

class FlashGame(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Slug', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    author = models.CharField(max_length=100, verbose_name='Автор')
    swf_file = models.FileField(
        upload_to='flash_games/',
        validators=[validate_swf_file],
        verbose_name='SWF файл'
    )
    thumbnail = models.ImageField(
        upload_to='flash_games/thumbnails/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name='Превью',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        GameCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='games',
        verbose_name='Категория'
    )
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    rating = models.FloatField(default=0.0, verbose_name='Рейтинг')
    total_ratings = models.IntegerField(default=0, verbose_name='Всего оценок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Флеш игра'
        verbose_name_plural = 'Флеш игры'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def add_rating(self, rating_value):
        if not 1 <= rating_value <= 5:
            raise ValueError('Рейтинг должен быть от 1 до 5')
        
        total = self.rating * self.total_ratings
        self.total_ratings += 1
        self.rating = (total + rating_value) / self.total_ratings
        self.save(update_fields=['rating', 'total_ratings'])

class GameRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_ratings', verbose_name='Пользователь')
    game = models.ForeignKey(FlashGame, on_delete=models.CASCADE, related_name='ratings', verbose_name='Игра')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Оценка игры'
        verbose_name_plural = 'Оценки игр'
        unique_together = ['user', 'game']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.game.name} - {self.rating}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.game.add_rating(self.rating)
