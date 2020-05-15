# -*- coding: utf-8 -*-
import requests, json
    
source_file_path = "/Users/shilei/Desktop/text.log"

url="http://127.0.0.1:8878/delete"

headers = {'Content-Type': 'application/json'}

data = {"file_name": "text.log", "file_path": "firmware/2020-04-07"}
session = requests.post(url, data=json.dumps(data), headers=headers)
print(session.text)