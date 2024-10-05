import asyncio
from aiohttp import ClientSession
from utils.url_params import BASE_ITEMS_RENDER_URL, QUERY_PARAMS
from schemas.response import Response
import requests

async def get_cur_page_data(params, session):
    async with session.get(url=BASE_ITEMS_RENDER_URL, params=params) as response:
        jsonn = await response.json()
        resp = Response(response.status, jsonn)
        return resp
    
async def get_data():
    async with ClientSession() as session:
        tasks = []
        for i in range(13):
            params = QUERY_PARAMS.copy()
            params["start"] = i * 100
            tasks.append(asyncio.create_task(get_cur_page_data(params, session)))

        data = await asyncio.gather(*tasks)
    
    return data


# async def get_data():
#     data = []
#     params = QUERY_PARAMS.copy()
#     for i in range(13):
#         params["start"] = i * 100
#         response = requests.post(url=BASE_ITEMS_RENDER_URL, params=params)
#         resp = Response(response.status_code, response.json())
#         data.append(resp)
#     return data