# Generated by Django 2.2.5 on 2020-06-22 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pages.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField()),
                ('duration', models.IntegerField(help_text='Duration to update price (in minutes)')),
                ('price_per_duration', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UserReviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=2000)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('rate', models.IntegerField()),
                ('user_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now=True)),
                ('bonus_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='pages.Bonus')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_bonus', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReservedTables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('table_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserved_times', to='pages.Table')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserved_tables', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, max_length=200, null=True, upload_to=pages.models.user_image_upload_path)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='custom_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
