# Generated by Django 4.2.1 on 2023-06-08 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_alter_project_options_alter_review_owner_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='review',
            name='owner',
        ),
    ]
