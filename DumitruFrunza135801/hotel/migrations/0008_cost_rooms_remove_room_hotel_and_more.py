# Generated by Django 4.0.6 on 2022-08-07 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0007_remove_room_cost_remove_room_start_period_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=5)),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('people', models.TextField()),
                ('size', models.DecimalField(decimal_places=0, max_digits=2)),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='room',
            name='hotel',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='rooms',
            new_name='rooms_count',
        ),
        migrations.DeleteModel(
            name='Reservation',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
        migrations.AddField(
            model_name='rooms',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel'),
        ),
        migrations.AddField(
            model_name='cost',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.rooms'),
        ),
    ]
