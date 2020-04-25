from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from aporte.models import Aporte#, Corrige
from .serializers import AporteSerializer#, CorrigeSerializer
# Create your views here.

# class AporteDeleteUpdate(RetrieveUpdateDestroyAPIView):
#     queryset = Aporte.objects.all()
#     serializer_class = AporteSerializer


# class AporteView(ListCreateAPIView):
#     queryset = Aporte.objects.all()
#     serializer_class = AporteSerializer

class AporteModelViewSet(ModelViewSet):
    queryset = Aporte.objects.all()
    serializer_class = AporteSerializer

# class CorrigeModelViewSet(ModelViewSet):
#     queryset = Corrige.objects.all()
#     serializer_class = CorrigeSerializer

 