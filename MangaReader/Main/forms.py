from django import forms
from .models import *


class UserListForm(forms.Form):
    list = forms.ModelChoiceField(queryset=List.objects.all(), required=False, widget=forms.Select(), empty_label=None, label='Добавить в коллекцию')

class MarkForm(forms.ModelForm):
    class Meta:
        model = UserMarkToManga
        exclude = ['user', 'manga']

class FilterForm(forms.Form):
    genre = forms.ModelMultipleChoiceField(Genre.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False, label='Жанр')
    type = forms.ModelMultipleChoiceField(Type.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False, label='Тип')
    status = forms.ModelMultipleChoiceField(Status.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False, label='Статус Тайтла')
    status_translate = forms.ModelMultipleChoiceField(Status.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False, label='Статус Перевода')

class SortForm(forms.Form):
    sort = forms.ChoiceField(choices=(ch:=[
        ('mark', 'Оценке'),
        ('mark_count', 'Количество оценок'),
        ('date_add', 'Дате добавления'),
        ('chapter_count', 'Количеству глав')]), 
        widget=forms.RadioSelect(), initial=ch[0],
        required=False, label='Сортировать по')
    order = forms.ChoiceField(choices=(ch:=[
        ('d', 'По убыванию'),
        ('a', 'По возрастанию')]), 
        widget=forms.RadioSelect(), initial=ch[0],
        required=False, label='Порядок сортировки')