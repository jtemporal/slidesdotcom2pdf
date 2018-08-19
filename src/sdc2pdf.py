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
    loop = True
    page = 1

    driver.fullscreen_window()
    while loop:
        time.sleep(10)
        screenshooting(driver, str(page).zfill(2))
        page += 1
        try:
            driver.find_element_by_class_name('navigate-down').click()
        except ElementNotInteractableException:
            loop = False
            print('fim da apresentação')

    driver.quit()


def topdf(filename='myslides'):
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = ('{}_{}{}'.format(now, filename, '.pdf'))
    images = []
    for (dirpath, dirnames, filenames) in os.walk('.'):
        images.extend(filenames)
        break
    images.sort()
    images = [image for image in images if 'screenshot' in image]
    pdf = FPDF('L', 'mm', (170, 297))
    pdf.set_margins(0,0,0)
    for image in images:
        pdf.add_page()
        pdf.image(image, y=10, w=297)
        print(image)
    pdf.output(filename, 'F')


def remove_temps():
    os.system('rm -rf *.png *.log') 


if __name__ == '__main__':
    decription = 'Create pdf files from slides.com presentation'
    parser = argparse.ArgumentParser(description=decription)
    parser.add_argument('slidesurl', metavar='s', type=str,
                        help='url for the slides')
    args = parser.parse_args()
    print('>>>>> iniciando captura da apresentação')
    main(args.slidesurl)
    print('>>>>> criando pdf')
    topdf()
    print('>>>>>> removendo intermediários')
    remove_temps()
    print('>>>>> the end')
