# -*- coding: utf-8 -*-
import os
import json
import time
import shutil
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Global Environment Variable
UPLOAD_FILE_PATH = os.getenv('UPLOAD_FILE_PATH')
NGINX_MIRROR_URL = os.getenv('NGINX_MIRROR_URL')
NGINX_MIRROR_STORAGE_PATH = os.getenv('NGINX_MIRROR_STORAGE_PATH')
REMOVE_SOURCE_FILE_SETUP = os.getenv('REMOVE_SOURCE_FILE_SETUP')

@csrf_exempt
def upload(request):
    request_params = request.POST
    file_name = request_params['file_name']
    file_path = request_params['file_path']
    file_md5 = request_params['file_md5']
    file_size = request_params['file_size']
    file_content_type = request_params['file_content_type']
    ip_address = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

    # 设置当前需要存储，以时间戳为名称的目录
    time_path = time.strftime("%Y-%m-%d", time.gmtime(time.time()))

    # 如果时间目录，不存在则创建目录
    if not os.path.exists(os.path.join(UPLOAD_FILE_PATH, NGINX_MIRROR_STORAGE_PATH, time_path)): os.makedirs(os.path.join(UPLOAD_FILE_PATH, NGINX_MIRROR_STORAGE_PATH, time_path))

    # 定义新的文件路径
    new_file_name = file_md5 + "_" + file_name
    new_file_path = os.path.join(UPLOAD_FILE_PATH, NGINX_MIRROR_STORAGE_PATH, time_path, new_file_name)
    old_file_name = file_name
    old_file_path = os.path.join(file_path)

    # 把 Nginx 存储的文件 Copy 到指定目录内，例：time_path/MD5_file_path
    shutil.copyfile(old_file_path, new_file_path)

    # 指定文件可被访问的 Url
    account_url = os.path.join(NGINX_MIRROR_URL, NGINX_MIRROR_STORAGE_PATH, time_path, new_file_name)

    # 是否删除 Nginx 源文件
    if REMOVE_SOURCE_FILE_SETUP:
        os.remove(file_path)

    ret = {
        'name': new_file_name,
        'path': new_file_path,
        'md5': file_md5,
        'size': file_size,
        'ip': ip_address,
        'content_type': file_content_type,
        'account_url': account_url,
    }
    return JsonResponse(ret)
