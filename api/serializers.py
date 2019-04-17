
from rest_framework import serializers
from aporte.models import Aporte

class AporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aporte
        fields = '__all__'