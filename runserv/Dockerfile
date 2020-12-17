FROM python:3.10.0a3-buster
RUN mkdir /source
RUN mkdir /logs
WORKDIR /source
ADD requirements.txt /source/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /source

RUN touch /reload
COPY runserv/entrypoint.sh /usr/bin/control
RUN chmod +x /usr/bin/control
ENTRYPOINT ["control"]