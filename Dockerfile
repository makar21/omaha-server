FROM python:3.7-slim-buster AS base

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -q -y --no-install-recommends \
    apt-utils \
    gnupg2 \
    wget && \
  rm -rf /var/lib/apt/lists/* && \
  wget -qO - https://openresty.org/package/pubkey.gpg | apt-key add - && \
  wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - && \
  echo "deb https://openresty.org/package/debian buster openresty" | tee -a /etc/apt/sources.list.d/openresty.list && \
  echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-6.x.list

RUN apt-get update && apt-get install -q -y --no-install-recommends \
    build-essential \
    filebeat \
    libmagic1 \
    libnginx-mod-http-lua \
    nginx \
    openresty \
    rsyslog \
    s3fs \
    supervisor \
    uwsgi-plugin-python3 && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /srv/omaha
RUN mkdir -p /srv/omaha_s3
COPY Pipfile Pipfile.lock /srv/omaha/
RUN pip install --no-cache-dir pipenv && \
  pipenv install --system --deploy --clear && \
  rm -rf /root/.cache/pip*

# RUN apt-get remove -q -y apt-utils build-essential gnupg2 wget && \
#   apt-get autoremove -q -y && \
#   rm -rf /var/lib/apt/lists/*

FROM base AS stable

COPY . /srv/omaha/

RUN \
  rm /etc/filebeat/filebeat.yml && \
  rm /etc/nginx/nginx.conf && \
  rm /etc/nginx/sites-enabled/default && \
  rm /etc/supervisor/supervisord.conf && \
  ln -s /srv/omaha/conf/nginx.conf /etc/nginx/ && \
  ln -s /srv/omaha/conf/nginx-app.conf /etc/nginx/sites-enabled/ && \
  ln -s /srv/omaha/conf/inflate_request.lua /usr/share/nginx/ && \
  ln -s /srv/omaha/conf/supervisord.conf /etc/supervisor/ && \
  ln -s /srv/omaha/conf/filebeat.yml /etc/filebeat/ && \
  chmod go-w /etc/filebeat/filebeat.yml

EXPOSE 80
EXPOSE 8080
CMD ["paver", "docker_run"]


FROM stable AS dev

RUN pipenv install --system --dev --clear && rm -rf /root/.cache/pip*
