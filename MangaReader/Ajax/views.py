from django.shortcuts import render
from django.views import View
from Main.forms import *
from Main.models import *
from django.http import JsonResponse
from django.db.models import *


class SetUserListView(View):
    def post(self, request):
        print(request.POST)

class SetMarkView(View):
    def post(self, request):
        print(request.POST)

class FilterView(View):
    def post(self, request):
        try: 
            if (g:=request.POST.getlist('genre')):
                genre = [Genre.objects.get(pk=id) for id in map(int, g)]
            else:
                genre = []

            if (t:=request.POST.getlist('ttype')):
                ttype = list(map(int, t))
            else:
                ttype = Type.objects.all()

            if (s:=request.POST.getlist('status')):
                status = list(map(int, s))
            else:
                status = Status.objects.all()

            if (st:=request.POST.getlist('status_translate')):
                status_translate = list(map(int, st))
            else:
                status_translate = Status.objects.all()

            sort = request.POST.getlist('sort')[0]
            order = request.POST.getlist('order')[0]

            if order == 'a':
                order = ''
            else:
                order = '-'

            mangaList = Manga.objects.all()

            for g in genre:
                mangaList = mangaList.filter(jenre=g)

            mangaList = mangaList.filter(type__in=ttype, 
                                         status__in=status, 
                                         status_translate__in=status_translate)
            
            if sort == 'chapter_count':
                mangaList = mangaList.annotate(chapter_count=
                                               Subquery(Chapter.objects.filter(manga=OuterRef('pk')).
                                                        values('manga').annotate(count=Count('id')).
                                                        values('count')))
                
            mangaList = mangaList.order_by(order + sort)

            return JsonResponse({'mangaList': list(mangaList.values())}, status=200)
        except Exception as ex:
            print(ex)
            return JsonResponse({}, status=200)
        
