# Generated by Django 4.2.7 on 2024-01-31 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_alter_productocreditogrupal_monto_credito_and_more'),
        ('users', '0058_alter_user_imagen_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='simulador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='simulador', to='dashboard.simulador'),
        ),
    ]
