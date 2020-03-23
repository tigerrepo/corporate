upstream django {
    server unix:///home/luchen/workspace/corporate/tiger/tiger.sock;
}

server {
    listen 80;
    server_name www.flinter.app flinter.app;
    location / {
        return 301 https://flinter.app$request_uri;
    }
}

server {
    listen      443;
    ssl on;

    ssl_certificate /etc/letsencrypt/live/flinter.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/flinter.app/privkey.pem;

    server_name flinter.app;
    access_log  /var/log/nginx/www.riceglobal.com.sg.access.log;
    error_log   /var/log/nginx/www.riceglobal.com.sg.error.log;

    location = / {
        return 301 index;
    }

    location /gallery {
        alias /var/www/cdn.riceglobal.com.sg/gallery;
    }
        
    location /video {
        alias /var/www/cdn.riceglobal.com.sg/video;
    }
     
    location /pdf {
        alias /var/www/cdn.riceglobal.com.sg/pdf;
    }
        
    location /logo {
        alias /var/www/cdn.riceglobal.com.sg/logo;
    }
    
    # FastCGI
    location / {
        uwsgi_pass django;
        include uwsgi_params;
    }

    location /static {
        # alias /var/www/www.riceglobal.com.sg/static/;
        alias /home/luchen/workspace/corporate/tiger/static/;
        autoindex off;
    }
}