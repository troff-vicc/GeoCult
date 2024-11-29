import asyncio
from ymaps import GeocodeAsync
import sqlite3
import base64

connection = sqlite3.connect('dataPlace.db')
cursor = connection.cursor()

with open('marshac.jpg', 'rb') as img:
    cursor.execute('INSERT INTO place (img) VALUES (?)', (base64.b64encode(img.read()),))

connection.commit()
connection.close()
'''
client = GeocodeAsync('83c8a581-d9c9-408b-8cbd-b8c1dd5d5238')


async def geocodeAddress(address):
    coordinate = await client.geocode(address)
    return coordinate["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(geocodeAddress('Воронеже, ул. Карла Маркса, 72')))
#Воронеж, ул. Орджоникидзе, 39
'''