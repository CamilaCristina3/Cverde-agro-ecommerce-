from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_producer_is_verified_producer_nif_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='two_factor_enabled',
            field=models.BooleanField(default=False, verbose_name='2FA por email'),
        ),
    ]
