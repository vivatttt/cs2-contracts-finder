import csv
from schemas import Item
from utils.adjusted_params import OUTPUT_FILE_NAME
from utils.generate_url import generate_url

async def write_data(array_items: list[Item]):
    with open(f'data/{OUTPUT_FILE_NAME}.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ')
        csvwriter.writerow(['name', 'url', 'ratio', 'price'])
        for item in array_items:
            row = [item.target_name, generate_url(item.target_name), item.ratio, item.price]
            csvwriter.writerow(row)