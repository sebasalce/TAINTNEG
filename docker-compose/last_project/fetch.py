import aiohttp
import asyncio

ENDPOINT_API = 'https://jobicy.com/api/v2/remote-jobs?count=1&tag=business%20intelligence'

async def fetch():
    async with aiohttp.ClientSession() as session:
        async with session.get(ENDPOINT_API) as res:
            if res.status == 200:
                dat = await res.json()
                print(dat)

asyncio.run(fetch())