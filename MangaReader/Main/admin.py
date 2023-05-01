from django.contrib import admin
from .models import *


admin.site.register(List)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(Genre)
admin.site.register(Manga)
admin.site.register(Chapter)
admin.site.register(ChapterToPhoto)
admin.site.register(UserToManga)

