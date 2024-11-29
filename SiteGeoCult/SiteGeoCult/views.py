from django.http import HttpResponseRedirect
from django.shortcuts import render
import json
import sqlite3
import random


def get_place_SQL(idTg):
    connection = sqlite3.connect('dataPlace.db')
    cursor = connection.cursor()
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
    idList = data[idTg]['place']
    listPlace = []
    for idPlace in idList:
        place = list(cursor.execute(f'SELECT * FROM place WHERE id={idPlace}').fetchone())
        place[3] = str(place[3])[2:-1]
        listPlace.append(place)
    return listPlace


def random_place():
    connection = sqlite3.connect('dataPlace.db')
    cursor = connection.cursor()
    count = cursor.execute(f'SELECT Count(id) FROM place').fetchone()
    idPlace = random.randint(0, int(count[0]) - 1)
    connection = sqlite3.connect('dataPlace.db')
    cursor = connection.cursor()
    place = list(cursor.execute(f'SELECT * FROM place WHERE id={idPlace}').fetchone())
    place[3] = str(place[3])[2:-1]
    return place

def index(request):
    return render(request, 'home.html')


def place(request):
    if request.COOKIES.get('id'):
        idTg = request.COOKIES.get('id')
    else:
        return HttpResponseRedirect('/')
    listPlace = get_place_SQL(idTg)
    return render(request, 'place.html', {'list_place': listPlace})


def geo(request):
    if not request.COOKIES.get('id'):
        return HttpResponseRedirect('/')
    randomPlace = random_place()
    return render(request, 'geo.html', {'place': randomPlace})


def map(request):
    if not request.COOKIES.get('id'):
        return HttpResponseRedirect('/')
    return render(request, 'map.html')