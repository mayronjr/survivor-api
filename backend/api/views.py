from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from sobreviventes.models import Sobrevivente, Reports
from sobreviventes.serializers import SobreviventeSerializer, ReportSerializer, SurvivorTradeSerializer

@api_view(['POST'])
def api_add_survivor(request, *args, **kwargs):

    survivor = SobreviventeSerializer(data=request.data)
    
    survivor.is_valid(raise_exception=True)
    survivor.save()

    return Response(survivor.validated_data, status=status.HTTP_201_CREATED)
            

@api_view(['GET'])
def api_get_all_survivor(request, *args, **kwargs):
    instances = Sobrevivente.objects.all()
    data = SobreviventeSerializer(many=True, instance=instances).data

    return Response(data)

@api_view(['GET'])
def api_get_one_survivor(request, id, *args, **kwargs):

    obj = get_object_or_404(Sobrevivente, pk=id)

    data = SobreviventeSerializer(instance=obj).data
    return Response(data)

@api_view(['PATCH'])
def api_update_survivor_location(request, id, *args, **kwargs):
    obj = get_object_or_404(Sobrevivente, pk=id)
    
    survivor = SobreviventeSerializer(instance=obj, data=request.data, partial=True)
    
    survivor.is_valid(raise_exception=True)
    survivor.save()

    return Response(survivor.validated_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def api_relate_infection(request, *args, **kwargs):
    report = ReportSerializer(data=request.data)

    report.is_valid(raise_exception=True)
    try:
        report = report.save()
    except IntegrityError:
        return Response({"message": "Você já reportou esse sobrevivente."}, status=status.HTTP_400_BAD_REQUEST)
    if Reports.objects.filter(reported=report.reported).count() >= 3 and not report.reported.is_infected:
        report.reported.is_infected = True
        report.reported.save(update_fields=['is_infected'])
        return Response({"message": "Sobrivivente reportado como infectado."}, status=status.HTTP_201_CREATED)
    return Response({"message": "Report foi feito."}, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def trade(request, *args, **kwargs):
    data = request.data
    instance = SurvivorTradeSerializer(data=request.data)
    instance.is_valid(raise_exception=True)
    data = instance.validated_data

    if data['recebendo'].get('sobrevivente').id == data['entregando'].get('sobrevivente').id:
        return Response({"message": "Não pode trocar com si mesmo."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if data['recebendo'].get('sobrevivente').is_infected or data['entregando'].get('sobrevivente').is_infected:
        return Response({"message": "Um ou ambos os sobreviventes estão infectados"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if calc_pontos(data['recebendo']) == calc_pontos(data['entregando']):
        
        sobrevivente_recebendo = data['recebendo'].get('sobrevivente').inventario
        if data['recebendo'].get('agua'):
            sobrevivente_recebendo.agua += data['recebendo'].get('agua')
        if data['recebendo'].get('alimentacao'):
            sobrevivente_recebendo.alimentacao += data['recebendo'].get('alimentacao')
        if data['recebendo'].get('medicacao'):
            sobrevivente_recebendo.medicacao += data['recebendo'].get('medicacao')
        if data['recebendo'].get('municao'):
            sobrevivente_recebendo.municao += data['recebendo'].get('municao')
        
        sobrevivente_entregando = data['entregando'].get('sobrevivente').inventario
        if data['entregando'].get('agua'):
            sobrevivente_entregando.agua -= data['entregando'].get('agua')
        if data['entregando'].get('alimentacao'):
            sobrevivente_entregando.alimentacao -= data['entregando'].get('alimentacao')
        if data['entregando'].get('medicacao'):
            sobrevivente_entregando.medicacao -= data['entregando'].get('medicacao')
        if data['entregando'].get('municao'):
            sobrevivente_entregando.municao -= data['entregando'].get('municao')

        sobrevivente_entregando.save()
        sobrevivente_recebendo.save()

        return Response({"message": "Troca feita"}, status=status.HTTP_200_OK)
    
    return Response({"message": "Troca não equivalente"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def calc_pontos(inventory):
    pontos = 0
    if inventory.get('agua'):
        pontos += inventory.get('agua') * 4
    if inventory.get('alimentacao'):
        pontos += inventory.get('alimentacao') * 3
    if inventory.get('medicacao'):
        pontos += inventory.get('medicacao') * 2
    if inventory.get('municao'):
        pontos += inventory.get('municao')
    return pontos
