from django import forms
from .models import *


class UserListForm(forms.Form):
    list = forms.ModelChoiceField(queryset=List.objects.all(), required=False, empty_label='Не в закладках', label='Добавить в коллекцию')

class FilterForm(forms.Form):
    genre = forms.ModelMultipleChoiceField(Genre.objects.all(), required=False, label='Жанр')
    type = forms.ModelMultipleChoiceField(Type.objects.all(), required=False, label='Тип')
    status = forms.ModelMultipleChoiceField(Status.objects.all(), required=False, label='Статус Тайтла')
    status_translate = forms.ModelMultipleChoiceField(Status.objects.all(), required=False, label='Статус Перевода')

class SortForm(forms.Form):
    sort = forms.ChoiceField(choices=[
        ('mark_count', 'Количество оценок'),
        ('mark', 'Оценке'),
        ('date_add', 'Дате добавления'),
        ('chapter_count', 'Количеству глав'),
    ], required=False, label='Сортировать по')
    order = forms.ChoiceField(choices=[
        ('a', 'По возрастанию'),
        ('d', 'По убыванию')
    ], required=False, label='Порядок сортировки')