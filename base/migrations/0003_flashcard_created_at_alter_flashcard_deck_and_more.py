# Generated by Django 5.1.5 on 2025-03-27 17:49

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_flashcarddeck_name_alter_flashcarddeck_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='flashcard',
            name='deck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flashcards', to='base.flashcarddeck'),
        ),
        migrations.AlterField(
            model_name='flashcard',
            name='tags',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
