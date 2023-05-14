from django.views import View
from Main.forms import *
from Main.models import *
from django.http import JsonResponse
from django.db.models import *
from django.contrib.auth.models import User


class SetUserListView(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                username = request.POST.get('user')
                manga_id = int(request.POST.get('manga'))
                userlist_id = int(request.POST.get('form[list]'))

                user = User.objects.get(username=username)
                manga = Manga.objects.get(pk=manga_id)
                userlist = List.objects.get(pk=userlist_id)
                
                try:
                    currentUserlist = UserToManga.objects.get(user=user, manga=manga)
                    currentUserlist.list = userlist
                except UserToManga.DoesNotExist:
                    currentUserlist = UserToManga(user=user, manga=manga, list=userlist)
                
                currentUserlist.save()
                
                return JsonResponse({}, status=200)
            except Exception as ex:
                print(ex)
                return JsonResponse({}, status=400)
            
class SetUserMarkView(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                username = request.POST.get('user')
                manga_id = int(request.POST.get('manga'))
                usermark = int(request.POST.get('form[mark]'))

                user = User.objects.get(username=username)
                manga = Manga.objects.get(pk=manga_id)
                
                try:
                    currentUsermark = UserMarkToManga.objects.get(user=user, manga=manga)
                    currentUsermark.mark = usermark
                except UserMarkToManga.DoesNotExist:
                    currentUsermark = UserMarkToManga(user=user, manga=manga, mark=usermark)

                print(manga.mark, manga.mark_count)
                #сделать оценку тут и при удалении
                #manga.mark = (manga.mark + usermark) / 2
                #manga.mark_count += 1

                print(manga.mark, manga.mark_count)

                currentUsermark.save()
                manga.save()
                
                return JsonResponse({}, status=200)
            except Exception as ex:
                print(ex)
                return JsonResponse({}, status=400)

class DeleteUserListView(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                username = request.POST.get('user')
                manga_id = int(request.POST.get('manga'))

                user = User.objects.get(username=username)
                manga = Manga.objects.get(pk=manga_id)
                
                try:
                    currentUserlist = UserToManga.objects.get(user=user, manga=manga)
                    currentUserlist.delete()
                except UserToManga.DoesNotExist:
                    pass
                
                return JsonResponse({}, status=200)
            except Exception as ex:
                print(ex)
                return JsonResponse({}, status=400)        

class DeleteUserMarkView(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                username = request.POST.get('user')
                manga_id = int(request.POST.get('manga'))

                user = User.objects.get(username=username)
                manga = Manga.objects.get(pk=manga_id)

                try:
                    currentUsermark = UserMarkToManga.objects.get(user=user, manga=manga)
                    currentUsermark.delete()
                except UserMarkToManga.DoesNotExist:
                    pass
                
                return JsonResponse({}, status=200)
            except Exception as ex:
                print(ex)
                return JsonResponse({}, status=400)

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
            return JsonResponse({}, status=400)
