import requests

def fetch_block_data(block_height):
    url = f"https://blockchain.info/block-height/{block_height}?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None