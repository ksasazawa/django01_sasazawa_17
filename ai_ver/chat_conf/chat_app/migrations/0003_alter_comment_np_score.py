# Generated by Django 4.1.3 on 2022-11-17 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0002_comment_np_label_comment_np_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='np_score',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]