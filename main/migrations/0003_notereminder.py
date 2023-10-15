# Generated by Django 4.2.6 on 2023-10-14 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_category_options_diarynote_due_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteReminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('reminder_interval', models.CharField(choices=[('Thirty_Minutes', 'Thirty Minutes'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly')], max_length=100)),
                ('reminder_message', models.TextField()),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.diarynote')),
            ],
            options={
                'verbose_name': 'NOTE REMINDER',
                'verbose_name_plural': 'NOTE REMINDERS',
            },
        ),
    ]