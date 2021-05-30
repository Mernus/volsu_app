FROM python:3.9

USER root

RUN apt-get update && apt-get upgrade -y
RUN apt-get --assume-yes install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo \
    "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

RUN apt-get update && apt-get upgrade -y
RUN apt-get --assume-yes install docker-ce docker-ce-cli containerd.io

RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
RUN ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

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

RUN useradd -m uranami
RUN usermod -aG docker uranami
RUN touch /reload

USER uranami

EXPOSE 8000
ENTRYPOINT ["entrypoint.sh"]
CMD ["uwsgi"]