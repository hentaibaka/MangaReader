# Generated by Django 4.2 on 2023-05-14 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_alter_usermarktomanga_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermarktomanga',
            name='mark',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=1, verbose_name='Оценка'),
        ),
    ]
