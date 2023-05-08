from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', (MainPageView.as_view()), name='main'),
    path('catalog/', CatalogPageView.as_view(), name='catalogpage'),
    path('manga/<slug:mangaSlug>/', (MangaPageView.as_view()), name='mangapage'),
    path('manga/<slug:mangaSlug>/<int:chapterNumber>/', (ReaderPageView.as_view()), name='readerpage'),
    path('user/<slug:username>/', (UserPageView.as_view()), name='userpage'),
]