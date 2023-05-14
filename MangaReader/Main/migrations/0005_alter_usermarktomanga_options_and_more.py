# Generated by Django 4.2 on 2023-05-14 15:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Main', '0004_alter_manga_jenre_usermarktomanga'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermarktomanga',
            options={'verbose_name': 'Оценка пользователя', 'verbose_name_plural': 'Оценки пользователей'},
        ),
        migrations.AlterUniqueTogether(
            name='usermarktomanga',
            unique_together={('user', 'manga')},
        ),
    ]
