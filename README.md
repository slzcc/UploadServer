# Upload Server

入口通过 Nginx 作为 Web 端处理所有请求数据。

## 简要使用说明

启动方式：

```
$ docker-compose up -d
```

启动完成后会在当前环境下开启 `http://127.0.0.1:8888` 端口，由此 api 进行上传、下载、删除。

## 上传

上传有两种方式一种通过访问 `http://127.0.0.1:8888/upload` 通过 from 表单上传，这种可自行操作测试。此方式可以结合其他程序对接 API。

curl 方式, 通过如下命令上传 text.log 文件作为测试:

```
$ curl --form "file=@text.log" http://127.0.0.1:8888/upload
{"name": "text.log", "path": "/storage/firmware/2020-04-07/text.log", "md5": "9492fe88f263d58e0b686885e8c98c0e", "size": "4", "ip": "172.22.0.1", "content_type": "application/octet-stream", "account_url": "http://127.0.0.1:8888/firmware/2020-04-07/text.log", "status": "success", "status_code": "200"}
```

> 上传成功后返回此文件的存储数据信息, 最终可通过 url 获取下载地址.
> 上传路径由 `NGINX_MIRROR_STORAGE_PATH` 默认上传路径和 `USE_TIEM_SUB_DIRECTORY` 以每天为目录作为存储路径，进行目录结构的创建。
> 如果配置 `USER_MD5_PREFIX` 为 True, 则会使用文件名的 MD5 值作为文件名(9492fe88f263d58e0b686885e8c98c0e_text.log).

文件路径上传时可进行自定义，可通过脚本进行测试:
```
$ python3 ClientUpload.py
{"name": "9492fe88f263d58e0b686885e8c98c0e_text.log", "path": "/storage/data/text/2020-04-07/9492fe88f263d58e0b686885e8c98c0e_text.log", "md5": "9492fe88f263d58e0b686885e8c98c0e", "size": "4", "ip": "172.22.0.1", "content_type": "multipart/form-data", "account_url": "http://127.0.0.1:8888/data/text/2020-04-07/9492fe88f263d58e0b686885e8c98c0e_text.log", "status": "success", "status_code": "200"}
```

> 上传时如果重复上传相同内容则会进行覆盖。

## 删除

删除可通过如下命令进行:

```
$ curl -H 'Content-Type: application/json' -XDELETE 127.0.0.1:8888/delete -d '{ "file_path": "firmware/2020-04-07/", "file_name": "text.log"}'
{"name": "text.log", "path": "firmware/2020-04-07", "status": "success", "is_delete": true}

# or

$ python3 ClientDelete.py
{"name": "text.log", "path": "firmware/2020-04-07", "status": "success", "is_delete": true}
```

> `file_name` 和 `file_path` 的参数必须有, 但可以单独配置删除目录还是删除文件, 删除目录时 `file_name` 请留空, 反之.

## 文件检测

在删除文件时，清闲确认文件是否存在.

```
$ curl -XHEAD http://127.0.0.1:8888/firmware/2020-04-07/text.log -I
HTTP/1.1 200 OK
Server: nginx/1.10.2
Date: Tue, 07 Apr 2020 12:47:02 GMT
Content-Type: application/octet-stream
Content-Length: 4
Last-Modified: Tue, 07 Apr 2020 12:13:37 GMT
Connection: keep-alive
ETag: "5e8c6e71-4"
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: *
Access-Control-Allow-Methods: GET,POST,OPTIONS,DELETE,HEAD,PUT
Accept-Ranges: bytes
```
