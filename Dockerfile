FROM brave/omaha-server-base:buster

ADD . $omaha

# setup all the configfiles
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
