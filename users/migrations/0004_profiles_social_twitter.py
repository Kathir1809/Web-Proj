# Generated by Django 4.2.3 on 2023-07-10 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profiles_location_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='social_twitter',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]