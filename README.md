# Slides.com to PDF

A simple script to print out each slide and turn it into a PDF file using Selenium.

## TODOs

Things to improve:

- Dockerfile isn't finished
- cleanup method (remove screenshots after pdf is generated)
- add right side scroll in the process
- improve page size genereation

## Usage

```
pip install -r requirements.txt
python src/sdc2pdf.py https://slides.com/jtemporal/cdcotidiano/#/
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
