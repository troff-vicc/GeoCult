import asyncio
from ymaps import GeocodeAsync

client = GeocodeAsync('83c8a581-d9c9-408b-8cbd-b8c1dd5d5238')


async def geocodeAddress(address):
    coordinate = await client.geocode(address)
    return coordinate["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(geocodeAddress('Санкт-Петербург, ул. Блохина, 15'))
    
