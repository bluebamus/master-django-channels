# Generated by Django 5.1.7 on 2025-03-26 14:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date', models.DateField(null=True)),
                ('time', models.TimeField(null=True)),
                ('has_been_seen', models.BooleanField(default=False, null=True)),
                ('from_who', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_who', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_name', models.TextField()),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
