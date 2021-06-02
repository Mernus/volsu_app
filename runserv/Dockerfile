FROM python:3.9

RUN mkdir /source
RUN mkdir /logs
WORKDIR /source

RUN pip install --upgrade pip
COPY . /source
ADD requirements.txt /source/requirements.txt
RUN pip install --no-cache-dir -Ur requirements.txt

RUN touch /reload

COPY runserv/entrypoint.sh /usr/local/bin/
RUN chmod 777 /usr/local/bin/entrypoint.sh && \
    ln -s /usr/local/bin/entrypoint.sh /

RUN apt-get update
RUN apt-get --assume-yes install nano \
                                 wget \
                                 dialog \
                                 net-tools \
                                 nginx
RUN rm -v /etc/nginx/nginx.conf && \
    cp runserv/nginx.conf /etc/nginx/nginx.conf
RUN service nginx start

EXPOSE 8000
ENTRYPOINT ["entrypoint.sh"]
CMD ["uwsgi"]