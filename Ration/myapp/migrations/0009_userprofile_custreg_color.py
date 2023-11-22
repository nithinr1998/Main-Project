# Generated by Django 4.2.6 on 2023-11-19 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_custreg_cardcolor_remove_custreg_cardtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('place', models.CharField(max_length=100)),
                ('houseno', models.IntegerField()),
                ('membersno', models.IntegerField()),
                ('cnumber', models.IntegerField()),
                ('type', models.CharField(choices=[('1', 'Choose Card'), ('APL', 'APL'), ('BPL', 'BPL')], max_length=3)),
                ('color', models.CharField(choices=[('1', 'Choose Color'), ('White', 'White'), ('Blue', 'Blue'), ('Pink', 'Pink'), ('Yellow', 'Yellow')], max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('ration_card', models.FileField(upload_to='ration_cards/')),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='custreg',
            name='color',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
