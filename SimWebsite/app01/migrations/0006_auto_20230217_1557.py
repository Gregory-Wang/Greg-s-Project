# Generated by Django 3.2 on 2023-02-17 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_auto_20230207_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prettynum',
            name='level',
            field=models.SmallIntegerField(choices=[(4, '4级'), (3, '3级'), (2, '2级'), (1, '1级')], default=1, verbose_name='级别'),
        ),
        migrations.AlterField(
            model_name='prettynum',
            name='status',
            field=models.SmallIntegerField(choices=[(2, '未占用'), (1, '已占用')], default=2, verbose_name='状态'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('detail', models.TextField(verbose_name='详情信息')),
                ('level', models.SmallIntegerField(choices=[(1, '紧急'), (2, '重要'), (3, '临时')], default=1, verbose_name='级别')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.admin', verbose_name='负责人')),
            ],
        ),
    ]
