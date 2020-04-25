
from rest_framework import serializers
from aporte.models import Aporte, Grupo#, Corrige

class AporteSerializer(serializers.ModelSerializer):
    grupo = serializers.CharField()

    class Meta:
        model = Aporte
        fields = '__all__'

    def to_representation(self, instance):
        data = super(AporteSerializer, self).to_representation(instance)
        data['selic'] = instance.present_value() or None
        data['grupo_name'] = instance.grupo.name or None
        return data

    def validate(self, data):
        grupo = data.get('grupo')
        try:
            grupo_id = Grupo.objects.get(name=grupo)
        except:
            g = Grupo(name=grupo)
            g.save()
            grupo_id = Grupo.objects.get(name=grupo)
        data.update({'grupo': grupo_id})
        return data

# class CorrigeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Corrige
#         fields = '__all__'

#     def to_representation(self, instance):
#         data = super(CorrigeSerializer, self).to_representation(instance)
#         data['selic'] = instance.present_value() or None
#         return data
