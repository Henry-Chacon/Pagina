# Generated by Django 4.2 on 2024-10-22 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_rename_price_orderitem_item_total_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='login_attempts',
            field=models.IntegerField(default=0),
        ),
    ]