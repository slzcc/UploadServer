# -*- coding: utf-8 -*-
import requests
    
source_file_path = "/Users/shilei/Desktop/jianli/html/resume.html"

url="http://47.95.219.151/upload"

files = {"file1": ("resume.html", open(source_file_path, 'rb'), "multipart/form-data")}

data = {"custom_path": "demo/123"}
session = requests.post(url, data=data, files=files)
print(session.text)