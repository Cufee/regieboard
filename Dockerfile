FROM ubuntu:18.04

RUN apt-get update && apt-get clean && apt-get install -y \
    x11vnc \
    xvfb \
    gnupg2 \
    fluxbox \
    wmctrl \
    && apt-get update && apt-get -y install python3-pip chromium-browser chromium-chromedriver \
    && pip3 install -U selenium

RUN useradd apps \
    && mkdir -p /home/apps

ADD bootstrap.sh /
ADD regieboard /home/apps/
RUN chown -v -R apps:apps /home/apps
CMD './bootstrap.sh'
