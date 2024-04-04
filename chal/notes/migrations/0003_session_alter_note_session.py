# Generated by Django 5.0.3 on 2024-04-03 16:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_note_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='note',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.session'),
        ),
    ]
