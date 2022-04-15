# Generated by Django 4.0.4 on 2022-04-15 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sobreviventes', '0002_alter_sobrevivente_agua'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sobrevivente',
            name='alimentacao',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='sobrevivente',
            name='latitude',
            field=models.DecimalField(decimal_places=5, max_digits=5),
        ),
        migrations.AlterField(
            model_name='sobrevivente',
            name='longitude',
            field=models.DecimalField(decimal_places=5, max_digits=5),
        ),
        migrations.AlterField(
            model_name='sobrevivente',
            name='medicacao',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='sobrevivente',
            name='municao',
            field=models.IntegerField(),
        ),
    ]