FROM debian:bullseye

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y openssl && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir -p /app/ssl
CMD ["openssl", "req", \
    "-x509", \
    "-nodes", \
    "-days", "365", \
    "-newkey", "rsa:2048", \
    "-keyout", "/app/ssl/private.key", \
    "-out", "/app/ssl/certificate.crt", \
    "-subj", "/C=FR/ST=State/L=City/O=Organization/CN=localhost"]
