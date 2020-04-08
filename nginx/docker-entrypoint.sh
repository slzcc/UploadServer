#!/bin/bash
 
UPLOAD_BACKEND_ADDRESS=${UPLOAD_BACKEND_ADDRESS:-http://127.0.0.1:8878}
NGINX_MIRROR_HOME=${NGINX_MIRROR_HOME:-/mirror}
 
mkdir -p $NGINX_MIRROR_HOME/_upload
 
# Set Nginx Module Config
cat > /usr/local/nginx/conf/vhosts/default.conf << EOF
server {
    listen *:80;
    client_body_buffer_size 512k;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header REMOTE_ADD \$remote_addr;
 
    location / {
        root   ${NGINX_MIRROR_HOME};
        index  index.html index.htm;
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
        charset utf-8,gbk;
    }
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
 
    location /upload {
 
        # Pass altered request body to this location
        upload_pass @upload_backend;
        upload_pass_args on;
 
        # Store files to this directory
        upload_store /tmp/nginx_upload;
 
        # Allow uploaded files to be read only by user
        upload_store_access user:rw group:rw all:rw;
        set \$upload_field_name "file";
 
        # Set specified fields in request body
        upload_set_form_field "\${upload_field_name}_name" \$upload_file_name;
        upload_set_form_field "\${upload_field_name}_content_type" \$upload_content_type;
        upload_set_form_field "\${upload_field_name}_path" \$upload_tmp_path;
 
        # Inform backend about hash and size of a file
        upload_aggregate_form_field "\${upload_field_name}_md5" \$upload_file_md5;
        upload_aggregate_form_field "\${upload_field_name}_size" \$upload_file_size;
 
        upload_pass_form_field "^.*\$";
 
        upload_limit_rate 0;
 
        # upload_cleanup 400 404 499 500-505;
 
    }
 
    location @upload_backend {
 
        proxy_pass ${UPLOAD_BACKEND_ADDRESS};
 
    }

    location /delete {
 
        proxy_pass ${UPLOAD_BACKEND_ADDRESS};
 
    }
 
    location = /favicon.ico {
        log_not_found off;
    }
}
EOF
 
# Set Nginx.conf
cat > /usr/local/nginx/conf/nginx.conf << EOF
worker_processes  1;
 
error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;
 
 
events {
    worker_connections  65535;
}
 
 
http {
    include       /usr/local/nginx/conf/mime.types;
    default_type  application/octet-stream;
 
    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Credentials true;
    add_header Access-Control-Allow-Headers *;
    add_header Access-Control-Allow-Methods GET,POST,OPTIONS,DELETE,HEAD,PUT;
 
    log_format  main  '\$remote_addr - \$remote_user [\$time_local] "\$request" '
                      '\$status \$body_bytes_sent "\$http_referer" '
                      '"\$http_user_agent" "\$http_x_forwarded_for"';
 
    access_log  /var/log/nginx/access.log  main;
 
    sendfile        on;
    #tcp_nopush     on;
    client_max_body_size 10240m;
    keepalive_timeout  300;
 
    #gzip  on;
 
    include vhosts/*.conf;
}
EOF
 
cat > $NGINX_MIRROR_HOME/_upload/index.html << EOF
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>Title</title>
    <link rel='stylesheet' href=''>
</head>
<body>
    <div class="row">
    <h2>Select files to upload</h2>
    <form name="upload" method="POST" enctype="multipart/form-data" action="/upload">
      <input type="file" name="file1"><br>
      <input type="submit" name="submit" value="Upload">
      <input type="hidden" name="test" value="value">
    </form>
</div>
<script type='text/javascript'></script>
<script type='text/javascript'>
</script>
</body>
</html>
EOF

# Start
exec /usr/local/nginx/sbin/nginx -g "daemon off;"