# Generated by Django 2.2.2 on 2019-07-13 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vei', '0002_proxy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proxy',
            options={'verbose_name': '代理', 'verbose_name_plural': '代理'},
        ),
        migrations.AlterField(
            model_name='proxy',
            name='proxy_type1',
            field=models.CharField(choices=[('1', 'HTTP'), ('2', 'HTTPS')], default='1', max_length=10, verbose_name='代理类型'),
        ),
        migrations.AlterField(
            model_name='proxy',
            name='proxy_type2',
            field=models.CharField(choices=[('1', '未知'), ('2', '高匿'), ('3', '普匿')], default='2', max_length=10, verbose_name='代理类型'),
        ),
    ]