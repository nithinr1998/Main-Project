# Generated by Django 5.0 on 2024-02-13 04:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ration_shop_app', '0018_product_assigned_month_alter_product_card_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryBoy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('vehicle_type', models.CharField(max_length=50)),
                ('registration_number', models.CharField(max_length=20)),
                ('delivery_zones', models.TextField()),
                ('availability_timings', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
