from rest_framework.viewsets import ModelViewSet
from aporte.models import Aporte  # , Corrige
# , CorrigeSerializer
from .serializers import AporteSerializer, WalletSerializer, MovimentSerializer
from rest_framework import mixins, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from wallet.models import Wallet, Moviment
import io
import csv
import pandas as pd
import json
# class AporteDeleteUpdate(RetrieveUpdateDestroyAPIView):
#     queryset = Aporte.objects.all()
#     serializer_class = AporteSerializer


# class AporteView(ListCreateAPIView):
#     queryset = Aporte.objects.all()
#     serializer_class = AporteSerializer

class AporteModelViewSet(ModelViewSet):
    queryset = Aporte.objects.all()
    serializer_class = AporteSerializer


class ImportWalletCsv(CreateAPIView):

    def create(self, request, *args, **kwargs):
        csv_request = request.FILES['file']
        data = csv_request.read().decode('latin')

        io_string = io.StringIO(data)
        next(io_string)
        for column in csv.reader(io_string, delimiter=';', quotechar='|'):
            print(column[0])

        return Response('asd')
# class CorrigeModelViewSet(ModelViewSet):
#     queryset = Corrige.objects.all()
#     serializer_class = CorrigeSerializer


class WalletModelViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return Wallet.objects.filter(user_id=self.request.user.id)


class PositionWallet(APIView):
    # permission_classes = [IsAuthenticated, ]
    def get(self, request, pk):
        wallet = Wallet.objects.get(id=pk)
        position = wallet.position()
        moviment_serialized = MovimentSerializer(position['moviments'], many=True)
        position['moviments'] = moviment_serialized.data
        return Response(position)
