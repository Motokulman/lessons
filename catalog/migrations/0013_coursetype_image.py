# Generated by Django 2.1.4 on 2018-12-27 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_remove_coursetype_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursetype',
            name='image',
            field=models.ImageField(help_text='Upload preview for this CourseType', null=True, upload_to=''),
        ),
    ]
