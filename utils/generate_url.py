from urllib.parse import urljoin, quote
from utils.url_params import BASE_ITEM_URL

def generate_url(postfix):
    return urljoin(BASE_ITEM_URL, quote(postfix))
