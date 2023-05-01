from django import forms
from .models import *


class UserListForm(forms.Form):
    list = forms.ModelChoiceField(queryset=List.objects.all(), required=True, empty_label='', label='Добавить в коллекцию')

class FilterForm(forms.Form):
    genre = forms.ModelMultipleChoiceField(Genre.objects.all(), required=False, label='Жанр')
    type = forms.ModelMultipleChoiceField(Type.objects.all(), required=False, label='Тип')
    status = forms.ModelMultipleChoiceField(Status.objects.all(), required=False, label='Статус Тайтла')
    status_translate = forms.ModelMultipleChoiceField(Status.objects.all(), required=False, label='Статус Перевода')

class SortForm(forms.Form):
    sort = forms.ChoiceField(choices=[
        ('cm', 'Количество оценок'),
        ('mk', 'Оценке'),
        ('ad', 'Дате добавления'),
        ('cc', 'Количеству глав'),
    ], required=False, label='Сортировать по')
    order = forms.ChoiceField(choices=[
        ('a', 'По возрастанию'),
        ('d', 'По убыванию')
    ], required=False, label='Порядок сортировки')