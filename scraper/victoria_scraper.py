from bs4 import BeautifulSoup as soup
import urllib.request
import os, sys

from selenium import webdriver

path_to_chromedriver = "/usr/bin/chromedriver"



if sys.version_info[0] > 2:
	from urllib.request import Request, urlopen
	from urllib.parse import quote_plus, urlparse, parse_qs
else:
	from urllib import quote_plus
	from urllib2 import Request, urlopen
	from urlparse import urlparse, parse_qs

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)

# headless
options.add_argument('headless')
# options.add_argument("start-maximized")
# options.add_argument("disable-infobars")
# # options.add_argument("--incognito");
# options.add_argument('--disable-gpu')
# options.add_argument("--disable-extensions")

# options.add_argument("--disable-impl-side-painting")
# options.add_argument("--disable-accelerated-2d-canvas'")
# options.add_argument("--disable-gpu-sandbox")
# # options.add_argument("--no-sandbox")
# options.add_argument("--disable-extensions")
# options.add_argument("--dns-prefetch-disable")

driver = webdriver.Chrome(path_to_chromedriver, chrome_options=options)

def get_products(view_item_url):
    
    driver.get(view_item_url)

    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.implicitly_wait(20)
    driver.quit()
    page_soup = soup(res, "html.parser")
    # with urllib.request.urlopen(view_item_url) as response:
    #     html = response.read()
    # soup_html = soup(html, "html.parser")
    print(page_soup)

url = "https://www.victoriassecret.com/vs/panties/bikinis/"
# url = "https://www.bancosantander.es/es/particulares/prestamos/prestamo-coche/simulador"
get_products(url)