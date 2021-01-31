# Generated by Django 3.1.5 on 2021-01-29 18:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='category',
            field=models.CharField(choices=[('sport', 'sport'), ('electronics', 'electronics'), ('home_appliances', 'home_appliances'), ('RENT', 'RENT'), ('OTHERS', 'OTHERS')], default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]