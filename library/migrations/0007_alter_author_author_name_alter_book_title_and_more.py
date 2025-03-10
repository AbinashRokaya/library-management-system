# Generated by Django 5.1.1 on 2024-11-09 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_alter_book_category_id_alter_book_publisher_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='author_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='publishers',
            name='publisher_name',
            field=models.CharField(max_length=100),
        ),
    ]
