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
        file_request = request.FILES['file']
        
        data = file_request.read()# .decode('latin') # not sure: read()?? MemorySecurity issue??!?
        # https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/

# Pretty sure I need to encapsulate this into a new method:
        if file_request.name.endswith('.csv'):
            io_string = io.StringIO(data.decode('latin'))
            next(io_string)
            df = pd.read_csv(io_string, header=0, skip_blank_lines=True, 
                         skipinitialspace=True,delimiter=';', encoding='latin-1',
                         usecols=[0,1,2,3], names=['ATIVO', 'DATA', 'QUANTIDADE', 'VALOR'])
        elif file_request.name.endswith('.xls') or file_request.name.endswith('.xlsx'):
            io_string = io.BytesIO(data)# StringIO(data)
            next(io_string)
            df = pd.read_excel(io_string)
        print(df) # For debug :P
# Same thing here:
        try: # try to prepare data... 
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 
            df['DATA']=pd.to_datetime(df['DATA'])
            df['VALOR']=df['VALOR'].map(lambda x: locale.atof(x.strip("R$")))    
        except:
            pass
        
        try: 
            for index, row in df.iterrows():
                ativo = Instrument.objects.get(tckrSymb=row["ATIVO"])
                data = row["DATA"]
                quantidade = row["QUANTIDADE"]
                total_investment = row["VALOR"]
                

                # TODO pegar o wallet do request: 
                wallet = Wallet.objects.get(id=3) 
                operacao = Moviment(instrument=ativo, wallet=wallet, date=data, quantity=quantidade, total_investment=total_investment)
                print(operacao.instrument)
                operacao.save()
            print("Foi pra carteira")
            # TODO Manda um update para a página com as alterações na wallet
            return Response('Sucesso!')
        except:
            print("Merda")
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
