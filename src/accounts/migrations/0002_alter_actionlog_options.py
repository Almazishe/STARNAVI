# Generated by Django 3.2.2 on 2021-05-06 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actionlog',
            options={'ordering': ('-created_at',), 'verbose_name': 'User action', 'verbose_name_plural': 'Users actions'},
        ),
    ]