
from rest_framework import serializers
from aporte.models import Aporte, Grupo

class AporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aporte
        fields = '__all__'

    def to_representation(self, instance):
        data = super(AporteSerializer, self).to_representation(instance)
        data['selic'] = instance.amount_mais_selic() or None
        data['grupo_name'] = instance.grupo.name or None
        return data


