from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MyModelSerializer
from rest_framework import status
import json


def get_balance(idTg):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        idChat = idTg
    if idChat in data:
        balance = data[idChat]['balance']
    else:
        with open('data.json', 'w') as json_file:
            balance = '500'
            data[idChat] = {'balance': '500', 'place': []}
            json.dump(data, json_file)
    return balance


class Balance(APIView):
    def post(self, request, format=None):
        serializer = MyModelSerializer(data=request.data)
        
        if serializer.is_valid():
            idTg = serializer.validated_data['idTg']
            return Response(get_balance(idTg), status=status.HTTP_201_CREATED)