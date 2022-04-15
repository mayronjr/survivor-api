from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

from sobreviventes.choices import SEXO_CHOICES
# Create your models here.

class Sobrevivente(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField(validators=[MinValueValidator(0)])
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)

    is_infected = models.BooleanField(default=False)

    latitude = models.DecimalField(max_digits=10, decimal_places=6, validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    longitude = models.DecimalField(max_digits=10, decimal_places=6, validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])

class Inventario(models.Model):
    agua = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    alimentacao = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    medicacao = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    municao = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    sobrevivente = models.OneToOneField(Sobrevivente, related_name="inventario", on_delete=models.CASCADE)

class Reports(models.Model):
    reported = models.ForeignKey(Sobrevivente, related_name="reported", on_delete=models.CASCADE)
    reporting = models.ForeignKey(Sobrevivente, related_name="reporting", on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(name="report", fields=['reported', 'reporting'])]