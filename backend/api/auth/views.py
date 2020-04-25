from rest_framework.generics import CreateAPIView
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler, jwt_response_payload_handler
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import SerializerUserCreateUpdate
from account.models import User


def create_jwt(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    response = jwt_response_payload_handler(token, user)
    return response


class CreateUser(CreateAPIView):
    """
    Api for register users
    """
    serializer_class = SerializerUserCreateUpdate
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwarg):
        serializer = SerializerUserCreateUpdate(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            user_create = User.objects.get(
                username=self.request.data['username'])
            token = create_jwt(user_create)
            return Response(token)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)