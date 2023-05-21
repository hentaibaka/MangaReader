from django.db import models
from .utils import *
from django.conf import settings

class List(models.Model):
    name = models.CharField(unique=True, max_length=32, blank=False, null=False, verbose_name='Название списка')

    class Meta:
        verbose_name_plural = 'Списки'
        verbose_name = 'Список'

    def __str__(self) -> str:
        return self.name
    
class Type(models.Model):
    name = models.CharField(unique=True, max_length=32, verbose_name="Тип")

    class Meta: 
        verbose_name_plural = 'Типы'
        verbose_name = 'Тип'

    def __str__(self) -> str:
        return self.name

class Status(models.Model):
    name = models.CharField(unique=True, max_length=32, verbose_name="Статус")

    class Meta: 
        verbose_name_plural = 'Статусы'
        verbose_name = 'Статус'

    def __str__(self) -> str:
        return self.name

class Genre(models.Model):
    name = models.CharField(unique=True, max_length=32, verbose_name="Жанр")

    class Meta: 
        verbose_name_plural = 'Жанры'
        verbose_name = 'Жанр'

    def __str__(self) -> str:
        return self.name
    
class Manga(models.Model):
    slug = models.SlugField(unique=True) 
    title = models.CharField(max_length=255, blank=False, null=False, verbose_name="Название") 
    description = models.TextField(blank=False, null=False, verbose_name="Описание") 
    photo = models.ImageField(upload_to=handle_manga_file, verbose_name="Обложка") 
    date_release = models. DateField(verbose_name="Дата выхода")
    date_add = models. DateField(auto_now_add=True, verbose_name="Дата добавления")
    type = models.ForeignKey(Type, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Тип") 
    jenre = models.ManyToManyField(Genre, blank=True, verbose_name="Жанры")
    status = models.ForeignKey(Status, related_name='Status', blank=False, null=True, on_delete=models.SET_NULL, verbose_name='Статус тайтла')
    status_translate = models.ForeignKey(Status, related_name="Status_translate", blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Статус перевода")
    mark = models.FloatField(default=0., verbose_name="Оценка") 
    mark_count=models.IntegerField(default=0, verbose_name="Количество оценок")
    author = models.CharField(max_length=64, blank=False, null=False, verbose_name="Автор") 
    artist = models.CharField(max_length=64, blank=False, null=False, verbose_name="Художник")

    class Meta: 
        verbose_name_plural = 'Манга'
        verbose_name = 'Манга'

    def __str__(self) -> str:
        return f"Slug: {self.slug}, Название: {self.title}"
    
class Chapter(models.Model): 
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, verbose_name="Манга") 
    number = models.IntegerField(blank=False, null=False, verbose_name="Номер главы") 
    name = models.CharField(max_length=64, blank=True, verbose_name="Название главы")
    date_add = models.DateField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name_plural = 'Главы'
        verbose_name = 'Глава'
        unique_together = ('manga', 'number')

    def __str__(self) -> str:
        return f"Манга: {self.manga},  Номер главы: {self.number}"
    
class ChapterToPhoto(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, blank=False, null=False, verbose_name="Глава") 
    photo = models.ImageField(upload_to=handle_chapter_file, blank=False, null=False, verbose_name="Страница манги") 
    number = models.IntegerField(blank=False, null=False, verbose_name="Номер страницы")

    class Meta:
        verbose_name_plural = 'Страницы глав'
        verbose_name = 'Страница главы'
        unique_together = ('chapter', 'number')

    def __str__(self) -> str:
        return f"Глава: {self.chapter}, Номер страницы: {self.number}"
    
class UserToManga(models. Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE, verbose_name="Пользователь") 
    manga = models.ForeignKey(Manga, blank=False, null=False, on_delete=models.CASCADE, verbose_name="Манга") 
    list = models.ForeignKey(List, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Список") 
    date_add = models.DateField(auto_now_add=True, null=False, blank=False, verbose_name="дата добавления в закладки")

    class Meta:
        verbose_name_plural = 'В закладках у пользователей'
        verbose_name = 'В закладках у пользователя'
        unique_together = ('user', 'manga')

    def __str__(self) -> str:
        return f"Манга: {self.manga}, Пользователь: {self.user}, Список: {self.list}"
    
class MarkChoices(models.IntegerChoices):
    ONE = (1, "1")
    TWO = (2, "2")
    THREE = (3, "3")
    FOUR = (4, "4")
    FIVE = (5, "5")
    SIX = (6, "6")
    SEVEN = (7, "7")
    EIGHT = (8, "8")
    NINE = (9, "9")
    TEN = (10, "10")

class UserMarkToManga(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE, verbose_name="Пользователь")
    manga = models.ForeignKey(Manga, blank=False, null=False, on_delete=models.CASCADE, verbose_name="Манга")
    mark = models.IntegerField(choices=MarkChoices.choices, default=MarkChoices.ONE, blank=False, null=False, verbose_name="Оценка")

    class Meta:
        verbose_name_plural = 'Оценки пользователей'
        verbose_name = 'Оценка пользователя'
        unique_together = ('user', 'manga')

    def __str__(self) -> str:
        return f"Манга: {self.manga} Пользователь: {self.user} Оценка: {self.mark}"
