# -*- coding: utf-8 -*-
import os
import json
import time
import shutil
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Global Environment Variable
## Storage Root Directory (/..)
UPLOAD_FILE_PATH = os.getenv('UPLOAD_FILE_PATH')
## Nginx Mirror Http Address (http://localhost/)
NGINX_MIRROR_URL = os.getenv('NGINX_MIRROR_URL')
## Store the Default Path ($NGINX_MIRROR_URL/$NGINX_MIRROR_STORAGE_PATH)
NGINX_MIRROR_STORAGE_PATH = os.getenv('NGINX_MIRROR_STORAGE_PATH')
## Whether or Not to Delete in Nginx Upload (/tmp/nginx_upload/..)
REMOVE_SOURCE_FILE_SETUP = os.getenv('REMOVE_SOURCE_FILE_SETUP')
## Whether to Add the Time Directory (../../2018-07-31/..)
USE_TIEM_SUB_DIRECTORY = os.getenv('USE_TIEM_SUB_DIRECTORY')


@csrf_exempt
def upload(request):
    try:
        file_name = request.POST.getlist('file_name', "")[0]
        file_path = request.POST.getlist('file_path', "")[0]
        file_md5 = request.POST.getlist('file_md5', "")[0]
        file_size = request.POST.getlist('file_size', "")[0]
        file_content_type = request.POST.getlist('file_content_type', "")[0]
        custom_path = request.POST.getlist('custom_path', "")
        ip_address = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

        # 是否设置当前需要存储以时间戳为名称的目录
        time_path = time.strftime("%Y-%m-%d", time.gmtime(time.time())) if USE_TIEM_SUB_DIRECTORY else ""
            
        # 判断存储目录是否存在，如果不存在则创建目录
        if not custom_path:
            if not os.path.exists(os.path.join(UPLOAD_FILE_PATH, NGINX_MIRROR_STORAGE_PATH, time_path)): os.makedirs(os.path.join(UPLOAD_FILE_PATH, NGINX_MIRROR_STORAGE_PATH, time_path))
            absolute_path = os.path.join(UPLOAD_FILE_PATH, NGINX_MIRROR_STORAGE_PATH, time_path)
        else:
            if not os.path.exists(os.path.join(UPLOAD_FILE_PATH, "/".join(custom_path), time_path)): os.makedirs(os.path.join(UPLOAD_FILE_PATH, "/".join(custom_path), time_path))
            absolute_path = os.path.join(UPLOAD_FILE_PATH, "/".join(custom_path), time_path)

        # 定义新的文件路径
        new_file_name = file_md5 + "_" + file_name
        new_file_path = os.path.join(absolute_path, new_file_name)
        old_file_name = file_name
        old_file_path = os.path.join(file_path)

        # 把 Nginx 存储的文件 Copy 到指定目录内，例：time_path/MD5_file_path
        shutil.copyfile(old_file_path, new_file_path)

        # 指定文件可被访问的 Url
        if not custom_path:
            account_url = os.path.join(NGINX_MIRROR_URL, NGINX_MIRROR_STORAGE_PATH, time_path, new_file_name)
        else:
            account_url = os.path.join(NGINX_MIRROR_URL, "/".join(custom_path, time_path, new_file_name)



        # 是否删除 Nginx 源文件
        if REMOVE_SOURCE_FILE_SETUP: os.remove(file_path)

        # 返回值
        ret = {
            'name': new_file_name,
            'path': new_file_path,
            'md5': file_md5,
            'size': file_size,
            'ip': ip_address,
            'content_type': file_content_type,
            'account_url': account_url,
            'status': "success",
            'status_code': "200",
        }
    except:
        ret = {
            'status': "failed",
            'status_code': "503",
            'describe': "The uploaded file format or required parameters are not correct, please try.",
        }
    return JsonResponse(ret)
