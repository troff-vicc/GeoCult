from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MyModelSerializer, PosSerializer, BuySerializer
from rest_framework import status
import json
import math
import sqlite3
DelX = (39.270428 - 39.180551) / (2619 - 914)
DelY = (51.712880 - 51.664407) / (1812 - 318)
listBuy = [400, 200, 300, 350]
listHad = ['cel.png', 'hat.png', 'tomas.png', 'shluap.png']


def get_had(idTg):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        idChat = idTg
        had = data[idChat]['had']
    hadN = []
    for h in had:
        hadN.append(listHad[int(h)])
    return hadN


def checkBuy(idBuy, idUser):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        idChat = idUser
        balance = data[idChat]['balance']
        had = data[idChat]['had']
    if int(balance) >= listBuy[int(idBuy)]:
        if not (idBuy in had):
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)
                data[idUser]['balance'] = str(int(data[idUser]['balance']) - listBuy[int(idBuy)])
                data[idUser]['had'] = data[idUser]['had'] + [idBuy]
            with open('data.json', 'w') as json_file:
                json.dump(data, json_file)
            return 'success'
        return 'already'
    return 'There are not enough funds'


def coordinate_place(id_place: int):
    connection = sqlite3.connect('dataPlace.db')
    cursor = connection.cursor()
    dataPlace:str = cursor.execute(f'SELECT coordinate FROM place WHERE id={id_place}').fetchone()[0]
    dataPlace.find(',')
    place_y = dataPlace[:dataPlace.find(',')]
    place_x = dataPlace[dataPlace.find(',')+1:]
    return place_y, place_x


def convert_cor(y, x):
    return 51.722721 - float(y)*DelY, 39.130576 + float(x)*DelX


def get_reward(coordinate, idPlace, idUser):
    place_y1, place_x1 = coordinate_place(idPlace)
    place_y2, place_x2 = coordinate
    dist = math.hypot(float(place_x2) - float(place_x1), float(place_y2) - float(place_y1))
    
    distM = int(73932 * dist)
    reward = int(1/(dist*20))
    
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        data[idUser]['balance'] = str(int(data[idUser]['balance']) + reward)
        if not (idPlace in data[idUser]['place']):
            data[idUser]['place'] = data[idUser]['place'] + [idPlace]
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)
    return reward, distM


def get_balance(idTg):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        idChat = idTg
    if idChat in data:
        balance = data[idChat]['balance']
    else:
        with open('data.json', 'w') as json_file:
            balance = '500'
            data[idChat] = {'balance': '500', 'place': [], "had": []}
            json.dump(data, json_file)
    return balance


class Balance(APIView):
    def post(self, request, format=None):
        serializer = MyModelSerializer(data=request.data)
        
        if serializer.is_valid():
            idTg = serializer.validated_data['idTg']
            
            return Response((get_balance(idTg), get_had(idTg)), status=status.HTTP_201_CREATED)


class Positions(APIView):
    def post(self, request, format=None):
        serializer = PosSerializer(data=request.data)
        if serializer.is_valid():
            posX = serializer.validated_data['posX']
            posY = serializer.validated_data['posY']
            idPlace = serializer.validated_data['idPlace']
            idUser = serializer.validated_data['idUser']
            
            lisDate = get_reward(convert_cor(posY, posX), idPlace, idUser)
            return Response(lisDate, status=status.HTTP_201_CREATED)


class Buy(APIView):
    def post(self, request, format=None):
        serializer = BuySerializer(data=request.data)
        if serializer.is_valid():
            idBuy = serializer.validated_data['idBuy']
            idUser = serializer.validated_data['idUser']
            checkB = checkBuy(idBuy, idUser)
            if checkB == 'success':
                return Response('Успешная покупку!', status=status.HTTP_201_CREATED)
            elif checkB == 'already':
                return Response('Уже куплено!', status=status.HTTP_201_CREATED)
            else:
                return Response('Не хватает средств!', status=status.HTTP_201_CREATED)
        