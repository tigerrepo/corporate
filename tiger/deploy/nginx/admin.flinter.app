upstream django_admin {
    server unix:///home/luchen/workspace/corporate_admin/tiger_admin/tiger_admin.sock;
}

server {
    listen       80;
    server_name  admin.flinter.app;
    location / {
        return 301 https://admin.flinter.app$request_uri;
    }
}

server {
    listen      443;
    ssl on;

    ssl_certificate /etc/letsencrypt/live/admin.flinter.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/admin.flinter.app/privkey.pem;

    server_name admin.flinter.app;
    access_log  /var/log/nginx/admin.riceglobal.com.access.log;
    error_log   /var/log/nginx/admin.riceglobal.com.error.log;

    # FastCGI
    location / {
        uwsgi_pass django_admin;
        include uwsgi_params;
    }

    location /static {
        # alias /var/www/admin.riceglobal.com/static/;
        alias /home/luchen/workspace/corporate_admin/tiger_admin/static/;
        autoindex off;
    }
}
