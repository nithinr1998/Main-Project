# Generated by Django 3.2.25 on 2024-03-20 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ration_shop_app', '0035_pay_payment_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatbotMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('response', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]