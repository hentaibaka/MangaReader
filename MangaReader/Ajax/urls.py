from django.urls import path
from .views import *


urlpatterns = [
    path('ajax/filter/', FilterView.as_view(), name='filterajax'),
    path('ajax/setmark/', SetMarkView.as_view(), name='setmarkajax'),
    path('ajax/setuserlist/', SetUserListView.as_view(), name='setuserlistajax'),
]