# Generated by Django 3.2.6 on 2021-08-05 16:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('data', models.JSONField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
