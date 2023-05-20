from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.core.cache import cache
import operator
from .forms import *


MAINPAGE_MANGA_COUNT = 8
MAINPAGE_MANGA_TIMEOUT = 5 * 60

class MyView:
    menu = (('Главная', 'main'), ('Каталог', 'catalogpage'))

def a():
    import os
    for n in range(11, 18):
        slug = 'Sono-Bisque-Doll-wa-Koi-wo-Suru'
        manga = Manga.objects.get(slug=slug)
        #chapter = Chapter.objects.get(manga=manga, number=n)
        chapter = Chapter(manga=manga, name='', number=n)
        chapter.save()
        photos = os.listdir(f'./media/images/manga/{slug}/{n}/')
        photos = sorted(photos, key=lambda x: int(x.split('.')[0]))
        oldphotos = photos
        photos = [f'{slug}_{n}_{i+1}.{v.split(".")[-1]}' for i, v in enumerate(photos)]
        for old, new in zip(oldphotos, photos):
            os.rename(f'./media/images/manga/{slug}/{n}/{old}', f'./media/images/manga/{slug}/{n}/{new}')
        photos = sorted(photos, key=lambda x: int(x.split("_")[-1].split(".")[0]))
        for i, photo in enumerate(photos):
            ch2ph = ChapterToPhoto(chapter=chapter, photo=f'images/manga/{slug}/{n}/{photo}', number=i+1)
            ch2ph.save()

class MainPageView(View):
    def get(self, request):
        """
        context = {
            'popular': list[Manga],
            'updated': list[Manga],
            'new': list[Manga],
        }
        """
        popular = []
        #popular = cache.get('popular')
        if not popular:
            popular = [m for m in Manga.objects.order_by('-mark_count')[:MAINPAGE_MANGA_COUNT]]
            cache.set('popular', popular, MAINPAGE_MANGA_TIMEOUT)

        updated = []
        #updated = cache.get('updated')
        if not updated:
            #переписать
            chapters = []
            for m in Manga.objects.all():
                try:
                    chapter = Chapter.objects.filter(manga=m).latest('date_add') 
                    chapters.append(chapter)
                except Chapter.DoesNotExist:
                    pass
                
            chapters = sorted(chapters, key=operator.attrgetter('date_add'))[::-1]

            updated = [ch.manga for ch in chapters[:MAINPAGE_MANGA_COUNT]]
            cache.set('updated', updated, MAINPAGE_MANGA_TIMEOUT)
        
        new = []
        #new = cache.get('new')
        if not new:
            new = Manga.objects.all().order_by('date_add')[::-1][:MAINPAGE_MANGA_COUNT]
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
            'filterForm': FilterForm,
            'sortForm': SortForm,
            'mangaList': list[Manga],
        }
        """

        filterForm = FilterForm()
        sortForm = SortForm()
        mangaList = Manga.objects.all().order_by('-mark')

        context = {
            'title': 'Каталог',
            'filterForm': filterForm,
            'sortForm': sortForm,
            'mangaList': mangaList,
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
            'markForm': MarkForm
        }
        """

        manga = Manga.objects.get(slug=mangaSlug)
        try:
            chapters = Chapter.objects.filter(manga=manga).order_by('number')
        except Chapter.DoesNotExist:
            chapters = [] 

        listForm = UserListForm()
        isUserList = False

        markForm = MarkForm()
        isUserMark = False

        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
    
            try:
                userlist = UserToManga.objects.get(user=user, manga=manga)
                listForm = UserListForm(initial={'list': userlist.list})
                isUserList = True
            except UserToManga.DoesNotExist:
                pass
    
            try:
                usermark = UserMarkToManga.objects.get(user=user, manga=manga)
                markForm = MarkForm(initial={"mark": usermark.mark})
                isUserMark = True
            except UserMarkToManga.DoesNotExist:
                pass

        context = {
            'title': manga.title,
            'manga': manga,
            'chapters': chapters,
            'listForm': listForm,
            'isUserList': isUserList,
            'markForm': markForm,
            'isUserMark': isUserMark,
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
            'REQUEST': request,
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

        context = {
            'title': user.username,
            'lists': userLists,
            'mainmenu': MyView.menu,
        }

        return render(request, 'main/userpage.html', context)