from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Sobrevivente(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    sexo = models.CharField(max_length=10, choices=[(1, 'Homem'), (2, 'Mulher')])
    
    # inventario = models.JSONField(default=dict)
    
    agua = models.IntegerField(default=0)
    alimentacao = models.IntegerField(default=0)
    medicacao = models.IntegerField(default=0)
    municao = models.IntegerField(default=0)
    
    # localizacao = ArrayField(models.DecimalField(max_digits=5, decimal_places=5, default=0.0), size=2, default=list)

    latitude = models.DecimalField(max_digits=5, decimal_places=5, default=0.0)
    longitude = models.DecimalField(max_digits=5, decimal_places=5, default=0.0)

    @property
    def ultima_localizacao(self):
        return (self.latitude, self.longitude)
    
    @property
    def inventario(self):
        return {
            "agua": self.agua,
            "alimentacao": self.alimentacao,
            "medicacao": self.medicacao,
            "municao": self.municao
        }
