# Generated by Django 3.1.2 on 2020-10-12 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fpage', '0002_song_is_favorite'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='album_logo',
            new_name='album_logo_link',
        ),
    ]
