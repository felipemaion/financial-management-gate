
from rest_framework import serializers
from aporte.models import Aporte, Grupo

class AporteSerializer(serializers.ModelSerializer):
    grupo = serializers.CharField()

    class Meta:
        model = Aporte
        fields = '__all__'

    def to_representation(self, instance):
        data = super(AporteSerializer, self).to_representation(instance)
        data['selic'] = instance.amount_mais_selic() or None
        data['grupo_name'] = instance.grupo.name or None
        return data

    def validate(self, data):
        grupo = data.get('grupo')
        grupo_id = Grupo.objects.get(name=grupo)
        data.update({'grupo': grupo_id})
        return data

