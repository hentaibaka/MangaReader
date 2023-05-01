from django.shortcuts import render
from django.views import View
from django.core.cache import cache
import operator
from .forms import *


MAINPAGE_MANGA_COUNT = 6

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

        popular = [m for m in Manga.objects.order_by('mark_count')[:MAINPAGE_MANGA_COUNT]]
        updated = [ch.manga 
                   for ch in sorted(list(Chapter.objects.filter(manga=m).earliest('date_add') 
                              for m in Manga.objects.all()), 
                              key=operator.attrgetter('date_add'))
                              [:MAINPAGE_MANGA_COUNT]]
        new = [m for m in Manga.objects.order_by('date_add')[:MAINPAGE_MANGA_COUNT]]

        context = {
            'title': 'Главная',
            'mainmenu': MyView.menu,
            'popular': popular,
            'updated': updated,
            'new': new,
        }
        print(1111)
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
    def get(self, request, manga):
        """
        context = {
            
        }
        """

        context = {
            'title': '',
            'mainmenu': MyView.menu,
        }

        return render(request, 'main/mangapage.html', context)
    
class ReaderPageView(View):
    def get(self, request, manga, chapter):
        """
        context = {
        
        }#
        """

        context = {
            'title': '',
            'mainmenu': MyView.menu,
        }

        return render(request, 'main/readerpage.html', context)
    
class UserPageView(View):
    def get(self, request, username):
        """
        context = {
        
        }
        """

        context = {
            'title': '',
            'mainmenu': MyView.menu,
        }

        return render(request, 'main/userpage.html', context)