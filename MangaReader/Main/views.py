from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.core.cache import cache
import operator
from .forms import *


MAINPAGE_MANGA_COUNT = 6
MAINPAGE_MANGA_TIMEOUT = 5 * 60

class MyView:
    menu = (('Главная', 'main'), ('Каталог', 'catalogpage'))

class MainPageView(View):
    def get(self, request):
        """
        context = {
            'popular': list[Manga]
            'updated': list[manga]
            'new': list[manga]
        }
        """

        popular = cache.get('popular')
        if not popular:
            popular = [m for m in Manga.objects.order_by('mark_count')[:MAINPAGE_MANGA_COUNT]]
            cache.set('popular', popular, MAINPAGE_MANGA_TIMEOUT)

        updated = cache.get('updated')
        if not updated:
            updated = [ch.manga 
                       for ch in sorted(list(Chapter.objects.filter(manga=m).earliest('date_add') 
                                  for m in Manga.objects.all()), 
                                  key=operator.attrgetter('date_add'))
                                  [:MAINPAGE_MANGA_COUNT]]
            cache.set('updated', updated, MAINPAGE_MANGA_TIMEOUT)
        
        new = cache.get('new')
        if not new:
            new = [m for m in Manga.objects.order_by('date_add')[:MAINPAGE_MANGA_COUNT]]
            cache.set('new', new, MAINPAGE_MANGA_TIMEOUT)

        context = {
            'title': 'Главная',
            'mainmenu': MyView.menu,
            'popular': popular,
            'updated': updated,
            'new': new,
        }
        
        return render(request, 'main/mainpage.html', context)
    
class CatalogPageView(View):
    def get(self, request):
        """
        context = {
            #запрос данных будет через AJAX
        }
        """

        context = {
            'title': 'Каталог',
            'mainmenu': MyView.menu,
        }
        return render(request, 'main/catalogpage.html', context)

class MangaPageView(View):
    def get(self, request, mangaSlug):
        """
        context = {
            'manga': Manga,
            'chapters': list[Chapter], #уже отстортированные по порядку
            'listForm': UserListForm,
        }
        """

        manga = Manga.objects.get(slug=mangaSlug)

        chapters = Chapter.objects.filter(manga=manga).order_by('number')

        listForm = UserListForm()

        context = {
            'title': manga.title,
            'manga': manga,
            'chapters': chapters,
            'listForm': listForm,
            'mainmenu': MyView.menu,
        }

        return render(request, 'main/mangapage.html', context)
    
class ReaderPageView(View):
    def get(self, request, mangaSlug, chapterNumber):
        """
        context = {
            'manga': Manga,
            'chapter': Chapter,
            'prevChapter': Chapter,
            'nextChapter': Chapter,
            'chapters': list[Chapter], #уже отстортированные по порядку
            'photos': list[ChapterToPhoto], #уже отстортированные по порядку
        }
        """

        manga = Manga.objects.get(slug=mangaSlug)

        chapter = Chapter.objects.get(manga=manga, number=chapterNumber)

        try:
            prevChapter = Chapter.objects.get(manga=manga, number=chapterNumber - 1)
        except Chapter.DoesNotExist:
            prevChapter = None

        try:    
            nextChapter = Chapter.objects.get(manga=manga, number=chapterNumber + 1)
        except Chapter.DoesNotExist:
            nextChapter = None

        chapters = Chapter.objects.filter(manga=manga).order_by('number')

        photos = ChapterToPhoto.objects.filter(chapter=chapter).order_by('number')

        context = {
            'title': f'{manga.title} глава {chapter.number}' + f' - {chapter.name}' if chapter.name else '',
            'manga': manga,
            'chapter': chapter,
            'prevChapter': prevChapter,
            'nextChapter': nextChapter,
            'chapters': chapters,
            'photos': photos,
            'mainmenu': MyView.menu,
        }

        return render(request, 'main/readerpage.html', context)
    
class UserPageView(View):
    def get(self, request, username):
        """
        context = {
            user: User,
            lists: dict[List, list[Manga]] #словарь, где ключи это объекты List, а значения это списки с мангой
                                               #нейминг гениальный, я знаю
        }
        """
        user = User.objects.get(username=username)
        
        lists = list(List.objects.all())

        manga2list = [UserToManga.objects.filter(user=user, list=l) for l in lists]

        userLists = dict(zip(lists, manga2list))
        print(userLists)

        context = {
            'title': user.username,
            'lists': userLists,
            'mainmenu': MyView.menu,
        }

        return render(request, 'main/userpage.html', context)