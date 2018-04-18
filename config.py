def create_config(domain, port, name):
    with open('/etc/nginx/sites-enabled/%s' % name, 'a+') as file:
        file.write("""
server {
    server_name %s;
    location / {
        proxy_pass http://127.0.0.1:%s;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
 # managed by Certbot

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/zusor.org-0001/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/zusor.org-0001/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

server {
    if ($host = %s) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    server_name %s;
    listen 80;
    return 404; # managed by Certbot


}
        """ %(domain, port, domain, domain))
