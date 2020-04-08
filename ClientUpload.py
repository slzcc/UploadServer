# -*- coding: utf-8 -*-
import requests
    
source_file_path = "/Users/shilei/Desktop/text.log"

url="http://127.0.0.1:8888/upload"

files = {"file1": ("text.log", open(source_file_path, 'rb'), "multipart/form-data")}

data = {"custom_path": "data/text"}
session = requests.post(url, data=data, files=files)
print(session.text)