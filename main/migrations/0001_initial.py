# Generated by Django 3.1.4 on 2021-05-20 08:12

import colorfield.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
import django.contrib.postgres.fields.citext
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields
import django_extensions.db.fields
import main.models.user
import main.validators
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=25, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator(), django.core.validators.MinLengthValidator(3)], verbose_name='Имя пользователя')),
                ('password', models.CharField(max_length=128, validators=[django.core.validators.MinLengthValidator(8)], verbose_name='password')),
                ('fullname', django_cryptography.fields.encrypt(models.CharField(default=None, max_length=100, null=True, unique=True, validators=[main.validators.FullnameValidator()], verbose_name='ФИО пользователя'))),
                ('organization', django_cryptography.fields.encrypt(models.CharField(default=None, max_length=120, null=True, validators=[main.validators.TitleValidator()], verbose_name='Организация'))),
                ('added', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
                ('timezone', timezone_field.fields.TimeZoneField(default='Europe/Moscow', verbose_name='Часовой пояс')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Почта пользователя')),
                ('level', models.IntegerField(choices=[(0, 'Пользователь'), (1, 'Организатор'), (2, 'Модератор'), (3, 'Администратор')], default=0, verbose_name='Уровень прав пользователя')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Может использовать админ сайт')),
                ('is_active', models.BooleanField(default=True, help_text='Активен ли пользователь. Используется вместо удаления объекта.', verbose_name='Активен')),
                ('profile_img', models.ImageField(blank=True, upload_to=main.models.user.profile_upload, verbose_name='Картинка профиля')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['-level', 'username'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', django.contrib.postgres.fields.citext.CICharField(max_length=20, unique=True, validators=[main.validators.TitleValidator()], verbose_name='Тег')),
                ('back_color', colorfield.fields.ColorField(default='#000000', max_length=18, verbose_name='Цвет бэкграунда тега')),
                ('title_color', colorfield.fields.ColorField(default='#FFFFFF', max_length=18, verbose_name='Цвет тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=100, unique=True, validators=[main.validators.TitleValidator()], verbose_name='Название события')),
                ('description', django_cryptography.fields.encrypt(models.TextField(default=None, max_length=450, null=True, verbose_name='Описание события'))),
                ('location', django_cryptography.fields.encrypt(models.CharField(default=None, max_length=300, null=True, verbose_name='Местоположение'))),
                ('website', models.CharField(max_length=150, null=True, verbose_name='Официальный вебсайт')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['author', 'title'])),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='Время и дата начала события')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='Время и дата конца события')),
                ('status', models.IntegerField(choices=[(0, 'Reconciliation'), (-1, 'Rejected'), (1, 'Waiting for start'), (2, 'In process'), (3, 'Already passed')], default=0, verbose_name='Статус события')),
                ('event_files', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(blank=True, verbose_name='Картинки события'), size=10)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Организатор события')),
                ('participants', models.ManyToManyField(blank=True, related_name='participants', to=settings.AUTH_USER_MODEL, verbose_name='Участники события')),
                ('tags', models.ManyToManyField(blank=True, to='main.Tag', verbose_name='Теги события')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
                'ordering': ['start_date'],
            },
        ),
    ]