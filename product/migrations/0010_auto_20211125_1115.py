# Generated by Django 3.2.9 on 2021-11-25 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_usershopadress_discription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usershopadress',
            name='complate',
        ),
        migrations.RemoveField(
            model_name='usershopadress',
            name='discription',
        ),
        migrations.RemoveField(
            model_name='usershopadress',
            name='email',
        ),
    ]
