FROM python:3-slim
RUN apt-get update && \
    apt-get install curl poppler-utils gcc bzip2 libgtk-3-0 libdbus-glib-1-2 libx11-xcb1 libxt6 -y && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

ENV FIREFOX_VERSION 56.0.2
ENV GECKODRIVER_VERSION v0.19.1

RUN curl -L https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/pt-BR/firefox-$FIREFOX_VERSION.tar.bz2 | tar xj &&\
    mv firefox /opt/firefox/ && ln -s /opt/firefox/firefox /usr/bin/firefox

RUN curl -L https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz | tar xz &&\
    mv geckodriver /usr/bin/geckodriver

RUN mkdir /tmp/result
RUN pip install -U pip

WORKDIR /app/
COPY src/requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY src/sdc2pdf.py .
ENTRYPOINT ["python", "sdc2pdf.py"]
