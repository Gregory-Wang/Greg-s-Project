# Generated by Django 4.1.7 on 2023-02-26 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_alter_prettynum_level_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prettynum',
            name='level',
            field=models.SmallIntegerField(choices=[(3, '3级'), (2, '2级'), (4, '4级'), (1, '1级')], default=1, verbose_name='级别'),
        ),
    ]