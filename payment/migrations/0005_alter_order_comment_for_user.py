# Generated by Django 4.0.6 on 2022-10-27 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_order_date_placed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comment_for_user',
            field=models.TextField(blank=True, default='Your Payment is processing, please wait for us to update the received amount.', max_length=250, null=True),
        ),
    ]
