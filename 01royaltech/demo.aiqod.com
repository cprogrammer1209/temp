server {
    server_name demo.aiqod.com;
    root /var/www/demo-frontend;

    autoindex off;
    index index.cgi index.html;
    error_page 404 /index.html;

    client_max_body_size 1000m;
    large_client_header_buffers 8 100m;

    # Timeout settings for long-running requests
    client_header_timeout 3600s;
    client_body_timeout 3600s;
    keepalive_timeout 3600s;
    proxy_connect_timeout 3600s;
    proxy_send_timeout 3600s;
    proxy_read_timeout 3600s;
    fastcgi_read_timeout 3600s;

    fastcgi_buffers 8 100m;
    fastcgi_buffer_size 100m;

    listen 443 ssl;
    listen [::]:443 ssl;

    ssl_certificate  /etc/letsencrypt/live/demo.aiqod.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/demo.aiqod.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        # Force HTTPS redirect
        if ($http_x_forwarded_proto != 'https') {
            rewrite ^ https://$host$request_uri? permanent;
        }

        add_header Cache-Control "no-store, no-cache, must-revalidate";
        try_files $uri $uri/ /index.html;
    }

    location /UPLOAD_FILES {
        autoindex off;
    }

    location /nginx_status {
        stub_status on;
        access_log off;
        allow 220.225.70.38;
        deny all;
    }

    # Apply timeout + buffering behavior to critical API routes
    location /aiqod-api {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_request_buffering off;
        proxy_buffering off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /adhigam-api {
        proxy_pass http://127.0.0.1:2001;
        proxy_http_version 1.1;
        proxy_request_buffering off;
        proxy_buffering off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket configs (unchanged)
    location /socket-api {
        proxy_pass http://127.0.0.1:2002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    location /socket-orch {
        proxy_pass http://127.0.0.1:2003;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # Other APIs (applied extended timeout support where relevant)
    location /gibots-api {
        proxy_pass http://127.0.0.1:2004;
        proxy_http_version 1.1;
        proxy_request_buffering off;
        proxy_buffering off;
    }

    location /gibots-orch {
        proxy_pass http://127.0.0.1:2005;
    }

    location /gibots-pyapi {
        proxy_pass http://127.0.0.1:2006;
    }

    location /gibots-api-schedule {
        proxy_pass http://192.168.1.7:2007;
    }

    location /gibots-reports-api {
        proxy_pass http://127.0.0.1:2008;
    }

    location /chatbot {
        proxy_pass http://127.0.0.1:2009;
    }

    location /gibots-pyimg {
        proxy_pass http://127.0.0.1:2010;
    }

    location /gibots-ocr {
        proxy_pass http://127.0.0.1:2011;
    }

    location /about {
        # commented out, no proxy_pass yet
    }

    location /table-detection {
        # commented out, no proxy_pass yet
    }

    include fastcgi.conf;
}