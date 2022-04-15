from rest_framework import serializers

from .models import Inventario, Sobrevivente

class InventarioCriacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields=[
            'agua',
            'alimentacao',
            'medicacao',
            'municao'
        ]

class SobreviventeSerializer(serializers.ModelSerializer):
    inventario = InventarioCriacaoSerializer()
    class Meta:
        model = Sobrevivente
        fields = [
            'nome',
            'idade',
            'sexo',
            'inventario',
            'latitude',
            'longitude',
            'is_infected'
        ]
        read_only_fields=['is_infected']
        
    def create(self, validated_data):

        inventario = validated_data.pop('inventario')
        
        sobrevivente = Sobrevivente.objects.create(**validated_data)
        Inventario.objects.create(**inventario, sobrevivente=sobrevivente)

        return sobrevivente