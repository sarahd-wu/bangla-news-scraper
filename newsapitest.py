import json
import os

def json_to_txt(json_data, txt_filename):
    with open(txt_filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(json.dumps(json_data, indent=4))

import requests
url = ('https://newsapi.org/v2/top-headlines?q=bangladesh&apiKey=5361488062004d029672591724dbd214')
response = requests.get(url)
json_to_txt(response.json(), 'output_file.json')