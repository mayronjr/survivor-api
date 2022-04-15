from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from sobreviventes.models import Sobrevivente
from sobreviventes.serializers import SobreviventeSerializer

@api_view(['POST'])
def api_add_survivor(request, *args, **kwargs):

    survivor = SobreviventeSerializer(data=request.data)
    
    survivor.is_valid(raise_exception=True)
    survivor.save()

    return Response(survivor.validated_data, status=status.HTTP_201_CREATED)
            

@api_view(['GET'])
def api_get_all_survivor(request, *args, **kwargs):
    instances = Sobrevivente.objects.all()    
    data = []
    
    for i in range(len(instances)):
        data.append(SobreviventeSerializer(instances[i]).data)

    return Response(data)

@api_view(['GET'])
def api_get_one_survivor(request, id, *args, **kwargs):

    obj = get_object_or_404(Sobrevivente, pk=id)

    data = SobreviventeSerializer(instance=obj).data
    return Response(data)