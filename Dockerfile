FROM omaha-server-base

ADD . $omaha

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
