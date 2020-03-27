FROM ubuntu-debootstrap:14.04 AS base

ARG DEBIAN_FRONTEND=noninteractive

RUN \
  apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys ABF5BD827BD9BF62 && \
  echo 'deb http://nginx.org/packages/ubuntu/ trusty nginx' | tee --append /etc/apt/sources.list && \
  apt-get update && \
  apt-get install -q -y --no-install-recommends python-pip python-dev python-lxml python-psycopg2 libpq-dev supervisor nginx liblua5.1-dev lua-zlib libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev python-pil build-essential libfuse-dev libcurl4-openssl-dev libxml2-dev mime-support automake libtool pkg-config libssl-dev wget tar jq && \
  apt-get clean && \
  apt-get autoremove -y && \
  rm -rf /var/lib/{apt,dpkg,cache,log}/  && \
  pip install uwsgi

RUN \
  wget https://github.com/s3fs-fuse/s3fs-fuse/archive/v1.84.tar.gz -O /usr/src/v1.84.tar.gz && \
  tar xvz -C /usr/src -f /usr/src/v1.84.tar.gz && \
  cd /usr/src/s3fs-fuse-1.84 && \
  ./autogen.sh && \
  ./configure --prefix=/usr && \
  make && \
  make install && \
  mkdir /srv/omaha_s3 && \
  rm -rf /usr/src/s3fs-fuse-1.84 && \
  rm /usr/src/v1.84.tar.gz

RUN mkdir -p /srv/omaha/requirements
WORKDIR /srv/omaha
COPY requirements/base.txt /srv/omaha/requirements/
RUN \
  pip install paver && \
  pip install --upgrade pip six && \
  pip install -r requirements/base.txt

# build lua module for nginx
RUN \
  cd /tmp && \
  NGINX_VERSION=`nginx -v 2>&1 | grep -o '[[:digit:]].*$'` && \
  wget http://nginx.org/download/nginx-$NGINX_VERSION.tar.gz && \
  tar -xzvf nginx-$NGINX_VERSION.tar.gz && \
  wget -qO- https://api.github.com/repos/openresty/lua-nginx-module/tags | jq '.[] | select(.name=="v0.10.13").tarball_url' | xargs wget -O lua-nginx-module.tar && \
  mkdir -p /tmp/lua-nginx-module && tar -xvf lua-nginx-module.tar -C /tmp/lua-nginx-module --strip-components=1 && \
  wget -qO- https://api.github.com/repos/simpl/ngx_devel_kit/tags | grep -m 1 tarball_url | cut -d '"' -f 4 | xargs wget -O ngx_devel_kit.tar && \
  mkdir -p /tmp/ngx_devel_kit && tar -xvf ngx_devel_kit.tar -C /tmp/ngx_devel_kit --strip-components=1 && \
  cd nginx-$NGINX_VERSION && \
  nginx -V 2>&1 | grep 'configure arguments: ' | cut -d ":" -f2 | xargs ./configure --add-dynamic-module=/tmp/ngx_devel_kit --add-dynamic-module=/tmp/lua-nginx-module && \
  make build && \
  cp objs/ndk_http_module.so /usr/lib/nginx/modules/ndk_http_module.so && \
  cp objs/ngx_http_lua_module.so /usr/lib/nginx/modules/ngx_http_lua_module.so && \
  cd /tmp && \
  rm -R /tmp/*


FROM base AS stable

COPY . /srv/omaha

# setup all the configfiles
RUN \
  mkdir /etc/filebeat/ && \
  mkdir /etc/nginx/sites-enabled/ && \
  rm -f /etc/filebeat/filebeat.yml && \
  rm -f /etc/nginx/conf.d/default.conf && \
  rm -f /etc/nginx/nginx.conf && \
  ln -s /srv/omaha/conf/nginx.conf /etc/nginx/ && \
  ln -s /srv/omaha/conf/nginx-app.conf /etc/nginx/sites-enabled/ && \
  ln -s /srv/omaha/conf/inflate_request.lua /etc/nginx/ && \
  ln -s /srv/omaha/conf/supervisord.conf /etc/supervisor/conf.d/ && \
  ln -s /srv/omaha/conf/filebeat.yml /etc/filebeat/ && \
  chmod go-w /etc/filebeat/filebeat.yml

EXPOSE 80
EXPOSE 8080
CMD ["paver", "docker_run"]
