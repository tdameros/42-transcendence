FROM postgres:16.0-bookworm

COPY healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/healthcheck.sh

EXPOSE 5432
