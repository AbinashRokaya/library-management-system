# Generated by Django 5.1.1 on 2024-11-09 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_students_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='students',
            old_name='name',
            new_name='user',
        ),
    ]
