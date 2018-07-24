from django.shortcuts import render
# -*- coding: utf-8 -*-
import os
import json
import base64
import hashlib
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
UPLOAD_FILE_PATH = '/storage/'
 
# '''获取文件的大小,结果保留两位小数，单位为MB'''
def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize, 2)
 
# '''获取文件的 MD5 值'''
def get_FileMD5(filePath):
    MD5_Object = hashlib.md5()
    maxbuf = 8192
    f = open(filePath,'rb')
    while True:
        buf = f.read(maxbuf)
        if not buf:
            break
        MD5_Object.update(buf)
    f.close()
    hash = MD5_Object.hexdigest()
    return  hash
 
# '''获取文件的 后缀'''
def get_FileSuffix(filePath):
    suffix = os.path.splitext(os.path.basename(filePath))[1].strip(".")
    return suffix
 
@csrf_exempt
def upload(request):
    request_params = request.POST
    file_name = request_params['file_name']
    file_path = request_params['file_path']
    file_md5 = request_params['file_md5']
    file_base64_content = request_params['file_content']
    ip_address = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')
    target_file_path = os.path.join(UPLOAD_FILE_PATH, file_path, file_name)
 
    # 如果目录不存在则创建目录
    if not os.path.exists(os.path.join(UPLOAD_FILE_PATH, file_path)): os.makedirs(os.path.join(UPLOAD_FILE_PATH, file_path))
 
    # 写入文件
    with open(target_file_path, 'wb') as f:
        f.write(base64.b64decode(file_base64_content))
 
    ret = {
        'name': file_name,
        'path': file_path,
        # 'md5': get_FileMD5(target_file_path),
        'md5': file_md5,
        'size': get_FileSize(target_file_path),
        'ip': ip_address,
        'content_type': get_FileSuffix(target_file_path),
    }
    return JsonResponse(ret)
