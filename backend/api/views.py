from rest_framework.viewsets import ModelViewSet
from aporte.models import Aporte
from rest_framework.decorators import action
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
from datetime import datetime
import locale


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
        print(request.user)
        try:
            wallet = Wallet.objects.get(id=int(request.data['wallet']), user=request.user)
        except:
            print("Wallet for this User not found.")
            return (0)
        print(wallet)
        # return Response('Que merda, ein?')
        file_request = request.FILES['file']

        data = file_request.read()  # .decode('latin') # not sure: read()?? MemorySecurity issue??!?
        # https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/

        # Pretty sure I need to encapsulate this into a new method:
        if file_request.name.endswith('.csv'):
            io_string = io.StringIO(data.decode('latin'))
            next(io_string)
            df = pd.read_csv(io_string, header=0, skip_blank_lines=True,
                             skipinitialspace=True, delimiter=';', encoding='latin-1',
                             usecols=[0, 1, 2, 3], names=['ATIVO', 'DATA', 'QUANTIDADE', 'VALOR'])
        elif file_request.name.endswith('.xls') or file_request.name.endswith('.xlsx'):
            io_string = io.BytesIO(data)  # StringIO(data)
            next(io_string)
            df = pd.read_excel(io_string)
        # print(df) # For debug :P
        # Same thing here,  should be a method (?):
        try:  # try to prepare data...
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            df['DATA'] = pd.to_datetime(df['DATA'])
            df['VALOR'] = df['VALOR'].map(lambda x: locale.atof(x.strip("R$")))
        except:
            pass

        try:
            for index, row in df.iterrows():
                instrument = Instrument.objects.get(tckrSymb=row["ATIVO"])
                date = row["DATA"]
                quantity = row["QUANTIDADE"]
                total_investment = row["VALOR"]
                # print("Wallet:", wallet)
                moviment = Moviment(instrument=instrument, wallet=wallet, date=date, quantity=quantity,
                                    total_investment=total_investment)
                # print(moviment.instrument)
                moviment.save()
            # print("Foi pra carteira")
            # TODO Manda um update redirecionando para a página com as alterações na wallet.
            return Response('Sucesso!')
        except:
            print("Ei, deu merda ao carregar no banco de dados.")
            return Response(0)


# class CorrigeModelViewSet(ModelViewSet):
#     queryset = Corrige.objects.all()
#     serializer_class = CorrigeSerializer


class WalletModelViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Wallet.objects.filter(user_id=self.request.user.id)

    def get_object(self):
        return Wallet.objects.filter(user_id=self.request.user.id)

    @action(detail=True, methods=['get'])
    def movements(self, request, pk):
        query = Moviment.objects.filter(wallet_id=pk, wallet__user=self.request.user)
        serialized_data = MovimentSerializer(query, many=True)
        return Response(serialized_data.data)


class PositionWallet(APIView):
    # permission_classes = [IsAuthenticated, ]
    def get(self, request, pk):
        wallet = Wallet.objects.get(id=pk)
        position = wallet.position()
        moviment_serialized = MovimentSerializer(position['moviments'], many=True)
        position['moviments'] = moviment_serialized.data
        return Response(position)
