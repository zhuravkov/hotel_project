# Generated by Django 4.0.5 on 2022-06-30 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0010_remove_order_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='price',
        ),
        migrations.AddField(
            model_name='category',
            name='price',
            field=models.PositiveSmallIntegerField(default=1000, verbose_name='Цена'),
            preserve_default=False,
        ),
    ]
