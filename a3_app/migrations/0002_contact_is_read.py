from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a3_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
