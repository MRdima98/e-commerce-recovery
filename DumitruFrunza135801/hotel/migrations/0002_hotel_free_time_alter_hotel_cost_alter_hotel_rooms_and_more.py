# Generated by Django 4.0.5 on 2022-07-20 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='free_time',
            field=models.TextField(default='ciao'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hotel',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=1000000),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='rooms',
            field=models.DecimalField(decimal_places=0, max_digits=1000),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='stars',
            field=models.DecimalField(decimal_places=0, max_digits=1),
        ),
    ]
