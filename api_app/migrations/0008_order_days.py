# Generated by Django 4.0.5 on 2022-06-30 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0007_order_done_order_paid_alter_order_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='days',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
    ]
