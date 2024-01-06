FROM nginx:1.25.3-bookworm

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y openssl && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/nginx/ssl
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt -subj "/C=FR/ST=State/L=City/O=Organization/CN=localhost"
COPY nginx.conf /etc/nginx/nginx.conf