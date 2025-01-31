# Generated by Django 3.2.18 on 2024-10-17 07:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authtoken', '0004_auto_20240927_1224'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='token',
            name='unique_device_id_not_null_blank',
        ),
        migrations.AlterUniqueTogether(
            name='token',
            unique_together={('user', 'device_id')},
        ),
    ]

