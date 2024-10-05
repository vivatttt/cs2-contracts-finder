import asyncio
from contracts import get_data, parse_data, find_best_contracts, write_data

async def main():
    data = await get_data()
    prices = await parse_data(data)
    items_array = await find_best_contracts(prices)
    await write_data(items_array)

if __name__ == '__main__':
    asyncio.run(main())