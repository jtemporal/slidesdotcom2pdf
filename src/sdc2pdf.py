import argparse
import os
import time
import datetime

from fpdf import FPDF
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver import FirefoxOptions


def setup(url):
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    wd = webdriver.Firefox(firefox_options=opts)
    time.sleep(2)

    try:
        wd.get(url)
    except WebDriverException:
        wd.quit()
        print('deu ruim lek')
    scripts = [
        "var el = document.getElementsByClassName('pill'); el[0].remove(); el[0].remove();",
        "var el = document.getElementsByClassName('kudos-button'); el[0].remove();",
        "var el = document.getElementsByClassName('progress'); el[0].remove();"
    ]
    for s in scripts:
        wd.execute_script(s)
    return wd


def screenshooting(d, page):
    # https://stackoverflow.com/a/15870708
    element = d.find_element_by_class_name('backgrounds') # find part of the page you want image of
    location = element.location
    size = element.size
    png = d.get_screenshot_as_png() # saves screenshot of entire page

    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']


    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save(f'screenshot_{page}.png') # saves new cropped image


def main(url):
    driver = setup(url)
    presentation = True
    page = 1

    driver.find_element_by_class_name('fullscreen-button').click()
    while presentation:
        time.sleep(2)
        screenshooting(driver, str(page).zfill(2))
        page += 1

        down = driver.find_element_by_class_name('navigate-down')
        right = driver.find_element_by_class_name('navigate-right')


        if down.is_enabled():
            down.click()
            time.sleep(2)
            screenshooting(driver, str(page).zfill(2))
            page += 1
            down = driver.find_element_by_class_name('navigate-down')

        if right.is_enabled() and not down.is_enabled():
            right.click()
            time.sleep(2)

        if not right.is_enabled() and not down.is_enabled():
            screenshooting(driver, str(page).zfill(2))
            presentation = False

    driver.quit()


def topdf(filename='myslides'):
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = ('/tmp/result/{}_{}{}'.format(now, filename, '.pdf'))
    images = []
    for (dirpath, dirnames, filenames) in os.walk('.'):
        images.extend(filenames)
        break
    images.sort()
    images = [image for image in images if 'screenshot' in image]

    # https://www.daniweb.com/posts/jump/1271752
    image_file = images[0]
    img = Image.open(image_file)
    width, height = img.size

    pdf = FPDF('L', 'mm', (height, width))
    pdf.set_margins(0,0,0)
    for image in images:
        pdf.add_page()
        pdf.image(image, y=0, w=width)
    pdf.output(filename, 'F')


def remove_temps():
    os.system('rm -rf *.png *.log')


if __name__ == '__main__':
    decription = 'Create pdf files from slides.com presentation'
    parser = argparse.ArgumentParser(description=decription)
    url = 'https://slides.com/jtemporal/test/#/'
    parser.add_argument('slidesurl', metavar='s', type=str,
            help='url for the slides', default=url)
    args = parser.parse_args()
    print('>>>>> iniciando captura da apresentação')
    main(args.slidesurl)
    print('>>>>> criando pdf')
    topdf()
    print('>>>>>> removendo intermediários')
    remove_temps()
    print('>>>>> the end')
