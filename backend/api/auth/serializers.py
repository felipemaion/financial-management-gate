from django.db.migrations import serializer
from rest_framework import serializers
from account.models import User


class SerializerUser(serializers.ModelSerializer):
    """
        Classe de Serialização do Model Usuario
    """

    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser')


class SerializerUserCreateUpdate(serializers.ModelSerializer):
    """
    Classe de Serialização do Model User para API de criação de usuário
    """
    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        exclude = ('user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser')

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            instance.save()
            return instance
        return instance

    def create(self, validated_data):
        user = super(SerializerUserCreateUpdate, self).create(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user