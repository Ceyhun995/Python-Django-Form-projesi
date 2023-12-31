# Generated by Django 4.2.3 on 2023-08-15 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('formapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=50, verbose_name='sebep')),
                ('date', models.DateField(auto_now=True, verbose_name='Banlanma Tarihi')),
                ('authorizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Banlayan')),
                ('suspect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Banlanan User')),
            ],
        ),
    ]
