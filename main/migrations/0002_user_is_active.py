# Generated by Django 3.1.4 on 2021-05-02 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Активен ли пользователь. Используется вместо удаления объекта.', verbose_name='Активен'),
        ),
    ]
