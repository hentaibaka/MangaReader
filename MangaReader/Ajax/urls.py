from django.urls import path
from .views import *


urlpatterns = [
    path('filter/', FilterView.as_view(), name='filterajax'),
    path('setusermark/', SetUserMarkView.as_view(), name='setusermarkajax'),
    path('setuserlist/', SetUserListView.as_view(), name='setuserlistajax'),
    path('deleteusermark/', DeleteUserMarkView.as_view(), name='deleteusermarkajax'),
    path('deleteuserlist/', DeleteUserListView.as_view(), name='deleteuserlistxjax')
]