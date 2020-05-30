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
from instrument.models import Instrument
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
        file_request = request.FILES['file']
        data = file_request.read()# .decode('latin') # not sure: read()?? MemorySecurity issue??!?
        # https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/

# Pretty sure I need to encapsulate this into a new method:
        try:
            io_string = io.StringIO(data.decode('latin'))
            next(io_string)
            df = pd.read_csv(io_string, header=["ATIVO","DATA", "QUANTIDADE", "VALOR"], skip_blank_lines=True, 
                         skipinitialspace=True,delimiter=';', encoding='latin-1')
        except:
            io_string = io.BytesIO(data)# StringIO(data)
            next(io_string)
            df = pd.read_excel(io_string)
        print(df) # For debug :P
# Same thing here:
        try:
            for index, row in df.iterrows():
                ativo = Instrument.objects.get(tckrSymb=row["ATIVO"])
                data = row["DATA"]
                quantidade = row["QUANTIDADE"]
                total_investment = row["VALOR"]
                # TODO pegar o wallet do request: 
                operacao = Moviment(instrument=ativo, wallet=wallet, date=data, quantity=quantidade, total_investment=total_investment)
                print(operacao.instrument)
                operacao.save()
            return Response('Sucesso!')
        except:
            return Response('Que merda, ein?')



        
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
    permission_classes = [IsAuthenticated, ]
    def get(self, request, pk):
        wallet = Wallet.objects.get(id=pk,user=request.user)
        position = wallet.position()
        moviment_serialized = MovimentSerializer(position['moviments'], many=True)
        position['moviments'] = moviment_serialized.data
        return Response(position)
