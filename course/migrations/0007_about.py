# Generated by Django 4.0.6 on 2022-07-15 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_course_course_feature_1_course_course_feature_2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_title', models.CharField(default='Abids lectures', max_length=100)),
                ('about_us', models.TextField(blank=True, max_length=500, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=20, null=True)),
                ('contact_email', models.CharField(blank=True, max_length=50, null=True)),
                ('facebook_link', models.CharField(blank=True, max_length=80, null=True)),
                ('twitter_link', models.CharField(blank=True, max_length=80, null=True)),
                ('instagram_link', models.CharField(blank=True, max_length=80, null=True)),
            ],
        ),
    ]
