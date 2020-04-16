FROM ubuntu:18.04

RUN apt-get update && apt-get clean && apt-get install -y \
    x11vnc \
    xvfb \
    gnupg2 \
    fluxbox \
    wmctrl \
    wget \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get -y install python3-pip google-chrome-stable \
    && pip3 install -U selenium

RUN useradd apps \
    && mkdir -p /home/apps

COPY bootstrap.sh /
COPY ../regieboard /home/apps/
RUN chown -v -R apps:apps /home/apps
#CMD './bootstrap.sh'
