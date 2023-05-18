from django.views import View
from Main.forms import *
from Main.models import *
from django.http import JsonResponse
from django.db.models import *
from django.contrib.auth.models import User


class LoadPagesView(View):
    def get(self, request):
        start = int(request.GET.get("start") or 0)
        end = int(request.GET.get("end") or start + 4)

        try:
            chapter_id = int(request.GET.get("chapter_id"))
        except Exception as ex:
            print(ex)
            return JsonResponse({}, status=400)
        
        try:
            chapter = Chapter.objects.get(pk=chapter_id)
        except Chapter.DoesNotExist:
            return JsonResponse({}, status=400)

        pages = ChapterToPhoto.objects.filter(chapter=chapter, number__in=list(range(start+1, end+2))).order_by("number")

        return JsonResponse(
            {
            "pages": list(pages.values()),
            "exists": pages.exists(),
            }, status=200)

class SetUserListView(View):
    def post(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                username = request.POST.get('user')
                manga_id = int(request.POST.get('manga'))
                print(request.POST.get('form[list]'))
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
                    if currentUsermark != usermark:
                        newMark = (manga.mark * manga.mark_count - currentUsermark.mark) / (manga.mark_count - 1)
                        manga.mark = newMark
                        manga.mark_count -= 1
                        
                        currentUsermark.mark = usermark
                    else:
                        return JsonResponse({}, status=200)
                except UserMarkToManga.DoesNotExist:
                    currentUsermark = UserMarkToManga(user=user, manga=manga, mark=usermark)

                newMark = (manga.mark * manga.mark_count + usermark) / (manga.mark_count + 1)
                manga.mark = newMark
                manga.mark_count += 1

                currentUsermark.save()
                manga.save()
                
                return JsonResponse({'mark': round(manga.mark, 2), 'mark_count': manga.mark_count}, status=200)
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
                    newMark = (manga.mark * manga.mark_count - currentUsermark.mark) / (manga.mark_count - 1)
                    manga.mark = newMark
                    manga.mark_count -= 1

                    manga.save()
                    currentUsermark.delete()
                    return JsonResponse({'mark': round(manga.mark, 2), 'mark_count': manga.mark_count}, status=200)
                except UserMarkToManga.DoesNotExist:
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
