from rest_framework.viewsets import ModelViewSet
from aporte.models import Aporte #, Corrige
from .serializers import AporteSerializer, WalletSerializer#, CorrigeSerializer
from rest_framework import mixins,viewsets
from wallet.models import Wallet
from rest_framework.permissions import IsAuthenticated

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


class WalletModelViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return Wallet.objects.filter(user_id=self.request.user.id)