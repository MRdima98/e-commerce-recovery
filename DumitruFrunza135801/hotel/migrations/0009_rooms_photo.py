# Generated by Django 4.0.6 on 2022-08-16 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0008_cost_rooms_remove_room_hotel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='photo',
            field=models.FileField(default=213, upload_to=''),
            preserve_default=False,
        ),
    ]