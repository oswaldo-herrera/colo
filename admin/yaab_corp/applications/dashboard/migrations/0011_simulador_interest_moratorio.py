# Generated by Django 4.2.7 on 2024-02-05 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_plazo_interes_moratorio'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulador',
            name='interest_moratorio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
