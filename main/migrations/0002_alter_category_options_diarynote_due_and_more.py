# Generated by Django 4.2.6 on 2023-10-14 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'CATEGORY', 'verbose_name_plural': 'CATEGORIES'},
        ),
        migrations.AddField(
            model_name='diarynote',
            name='due',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='diarynote',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_note', to=settings.AUTH_USER_MODEL),
        ),
    ]