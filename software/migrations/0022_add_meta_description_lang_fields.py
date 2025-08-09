from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('software', '0021_category_is_published_category_meta_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='softwarecategory',
            name='meta_description_ar',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='softwarecategory',
            name='meta_description_de',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='softwarecategory',
            name='meta_description_en',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='softwarecategory',
            name='meta_description_es',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='softwarecategory',
            name='meta_description_fr',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='softwarecategory',
            name='meta_description_ru',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='softwarecategory',
            name='meta_description_zh_hans',
            field=models.TextField(null=True, blank=True),
        ),
    ]
