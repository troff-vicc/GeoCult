from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MyModelSerializer, PosSerializer, BuySerializer
from rest_framework import status
import json
import math
import sqlite3
DelX = (51.757494 - 51.614306) / 4191
DelY = (39.097896 - 39.333832) / 4473
listBuy = [400, 200, 300, 350]


def checkBuy(idBuy, idUser):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        idChat = idUser
        balance = data[idChat]['balance']
    if int(balance) >= listBuy[int(idBuy)]:
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
            data[idUser]['balance'] = str(int(data[idUser]['balance']) - listBuy[int(idBuy)])
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)
        return True
    return False


def coordinate_place(id_place: int):
    connection = sqlite3.connect('dataPlace.db')
    cursor = connection.cursor()
    dataPlace:str = cursor.execute(f'SELECT coordinate FROM place WHERE id={id_place}').fetchone()[0]
    dataPlace.find(',')
    place_y = dataPlace[:dataPlace.find(',')]
    place_x = dataPlace[dataPlace.find(',')+1:]
    return place_x, place_y


def convert_cor(x, y):
    return float(x)*DelX, float(y)*DelY


def get_reward(coordinate, idPlace, idUser):
    place_x1, place_y1 = coordinate_place(idPlace)
    place_x2, place_y2 = coordinate
    dist = math.hypot(float(place_x2) - float(place_x1), float(place_y2) - float(place_y1))
    distM = int(28114 * dist)
    reward = int(1/dist*2140)
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        data[idUser]['balance'] = str(int(data[idUser]['balance']) + reward)
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)
    return distM, reward


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


class Positions(APIView):
    def post(self, request, format=None):
        serializer = PosSerializer(data=request.data)
        if serializer.is_valid():
            posX = serializer.validated_data['posX']
            posY = serializer.validated_data['posY']
            idPlace = serializer.validated_data['idPlace']
            idUser = serializer.validated_data['idUser']
            
            lisDate = get_reward(convert_cor(posX, posY), idPlace, idUser)
            return Response(lisDate, status=status.HTTP_201_CREATED)


class Buy(APIView):
    def post(self, request, format=None):
        serializer = BuySerializer(data=request.data)
        if serializer.is_valid():
            idBuy = serializer.validated_data['idBuy']
            idUser = serializer.validated_data['idUser']
            if checkBuy(idBuy, idUser):
                return Response('Успешная покупку!', status=status.HTTP_201_CREATED)
            else:
                return Response('Не хватает средств!', status=status.HTTP_201_CREATED)
        