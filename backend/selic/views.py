from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from selic.models import Selic
# Create your views here.


class Corrige(APIView):
    def get(self, request):
        
        request = request.GET

        amount = request['amount']
        date = request['date']
        if 'final_date'in request:
            final_date = request['final_date']
        else:
            final_date = None
        
        selic = Selic.present_value(amount,date, final_date)
       
        return Response(selic)
