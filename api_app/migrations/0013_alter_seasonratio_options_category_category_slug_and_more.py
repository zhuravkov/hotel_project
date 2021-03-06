# Generated by Django 4.0.5 on 2022-07-08 08:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0012_seasonratio'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seasonratio',
            options={'ordering': ['start_date'], 'verbose_name': 'Сезонный коэффициент', 'verbose_name_plural': 'Сезонные коэффициенты'},
        ),
        migrations.AddField(
            model_name='category',
            name='category_slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=70, verbose_name='URL'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='done',
            field=models.BooleanField(default=False, verbose_name='Заказ исполнен'),
        ),
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Заказ оплачен'),
        ),
    ]
