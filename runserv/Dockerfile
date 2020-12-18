FROM python:3.9

RUN mkdir /source
RUN mkdir /logs
WORKDIR /source

RUN pip install --upgrade pip
COPY . /source
ADD requirements.txt /source/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN touch /reload

RUN mkdir -p ../media
RUN mkdir -p ../static

COPY runserv/entrypoint.sh /usr/local/bin/
RUN ln -s /usr/local/bin/entrypoint.sh /

EXPOSE 8080
ENTRYPOINT ["entrypoint.sh"]
CMD ["uwsgi"]