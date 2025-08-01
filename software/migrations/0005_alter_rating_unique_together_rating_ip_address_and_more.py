# Generated by Django 5.1.7 on 2025-06-25 23:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0004_rating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='rating',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, help_text='IP address of the user who submitted the rating.', null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(blank=True, help_text='The logged-in user who submitted the rating (optional for anonymous ratings).', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('software', 'ip_address')},
        ),
    ]
