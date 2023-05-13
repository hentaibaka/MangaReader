from django.urls import path
from .views import *


urlpatterns = [
    path('filter/', FilterView.as_view(), name='filterajax'),
    path('setmark/', SetMarkView.as_view(), name='setmarkajax'),
    path('setuserlist/', SetUserListView.as_view(), name='setuserlistajax'),
]