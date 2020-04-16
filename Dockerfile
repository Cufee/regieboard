<<<<<<< HEAD
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
=======
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
>>>>>>> 2e5c168c08c45db262e46a45f628505cd24204fb
