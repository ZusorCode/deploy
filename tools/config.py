def create_config(domain, port):
    with open('/etc/nginx/sites-enabled/%s' % repository, 'a+') as file:
        file.write("""
server {
    server_name %s;
    location / {
        proxy_pass http://127.0.0.1:%s;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
        """ %(domain, port))
