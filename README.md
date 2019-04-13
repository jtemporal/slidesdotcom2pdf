# Slides.com to PDF [![Build Status](https://travis-ci.com/jtemporal/slidesdotcom2pdf.svg?branch=master)](https://travis-ci.com/jtemporal/slidesdotcom2pdf)

A simple script to print out each slide and turn it into a PDF file using Selenium.

## TODOs

Things to improve:

- cleanup method (remove screenshots after pdf is generated)
- improve page size genereation

## Usage

### With Docker

Docker is the recommended way to use this.

```
docker pull slidesdotcom2pdf
docker run --rm --name sdc -v $(pwd)/slides:/tmp/result slidesdotcom2pdf http://slides.com/jtemporal/test
```

### Without Docker

```
pip install -r requirements.txt
python src/sdc2pdf.py http://slides.com/jtemporal/test
```

You'll also need geckodriver and firefox installed:

- for geckodriver:

```
curl -L https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz | tar xz && sudo mv geckodriver /usr/bin/geckodriver
```

- for firefox:

```
curl -L https://download-installer.cdn.mozilla.net/pub/firefox/releases/56.0.2/linux-x86_64/pt-BR/firefox-$FIREFOX_VERSION.tar.bz2 | tar xj && sudo mv firefox /opt/firefox/ && ln -s /opt/firefox/firefox /usr/bin/firefox
```
