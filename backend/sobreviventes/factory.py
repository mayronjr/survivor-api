from random import choice

import factory
from faker import Faker

from sobreviventes.choices import (
    SEXO_CHOICES
)
from sobreviventes.models import Sobrevivente, Inventario

fake = Faker()

class SobreviventeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sobrevivente

    def __init__(self):
        self.nome = fake.name()
    nome = factory.LazyAttribute(lambda _: fake.name())
    idade = factory.LazyAttribute(lambda _: fake.pyint(min_value=0))
    sexo = factory.LazyAttribute(lambda _: choice(SEXO_CHOICES)[0])

    latitude = factory.LazyAttribute(lambda _: fake.pydecimal(left_digits=3, right_digits=6, min_value=-90, max_value=90))
    longitude = factory.LazyAttribute(lambda _: fake.pydecimal(left_digits=3, right_digits=6, min_value=-180, max_value=180))

    # inventario = factory.LazyAttribute(lambda _: InventarioFactory())

class InventarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Inventario
    
    agua = factory.LazyAttribute(lambda _: fake.pyint(min_value=0, max_value=10))
    alimentacao = factory.LazyAttribute(lambda _: fake.pyint(min_value=0, max_value=10))
    medicacao = factory.LazyAttribute(lambda _: fake.pyint(min_value=0, max_value=10))
    municao = factory.LazyAttribute(lambda _: fake.pyint(min_value=0, max_value=10))

    sobrevivente = factory.SubFactory(SobreviventeFactory)