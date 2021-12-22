# Generated by Django 3.2.6 on 2021-11-05 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.ManyToManyField(blank=True, null=True, related_name='_product_comment_comment_+', to='product.Comment'),
        ),
    ]