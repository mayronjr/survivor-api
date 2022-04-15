from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from sobreviventes.models import Sobrevivente, Reports
from sobreviventes.serializers import SobreviventeSerializer, ReportSerializer

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
