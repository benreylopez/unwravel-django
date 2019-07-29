from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import base64
import json
from collections import Counter
import pandas as pd
import csv
from urllib.request import urlopen, Request

opts = webdriver.ChromeOptions()
opts.add_argument("--headless")
# opts.add_argument("disable-infobars")
# options.add_argument("--incognito");
# opts.add_argument('--disable-gpu')
# opts.add_argument("--disable-extensions")
# opts.add_argument("--disable-impl-side-painting")
# opts.add_argument("--disable-accelerated-2d-canvas'")
# opts.add_argument("--disable-gpu-sandbox")
opts.add_argument("--no-sandbox")
# opts.add_argument("--disable-extensions")
# opts.add_argument("--dns-prefetch-disable")
#opts.add_argument("--disable-dev-shm-usage")

total_product_number = 0
all_products = []

def zaful_scraper_test():
	product_api_path = "https://www.zaful.com/datafeed/Firstgrabber_data_feed_.csv"
	# data = pd.read_csv("https://www.zaful.com/datafeed/Firstgrabber_data_feed_.csv")
	# data.head()
	# print("data:", data.head())

	with urllib.request.urlopen(product_api_path) as response:
		detailed_information = response.read()
	print(detailed_information)

def zaful_scraper():
	print("zaful products scraping started ....")
	global all_products
	global total_product_number
	total_product_number = 0
	all_products = []
	driver = webdriver.Chrome('chromedriver', options=opts)
	path = "static/victoria_secret_temp.json"
	json_data = open(path)
	all_products = json.load(json_data)
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}

	product_api_path = "https://www.zaful.com/datafeed/Firstgrabber_data_feed_.csv"
	req = Request(url=product_api_path, headers=headers)
	# response = urlopen(req).read()
	# csvfile = csv.reader(urlopen(req).read().decode('utf-8'))
	pd_products = pd.read_csv(urlopen(req))
	# pd_products = pd.read_csv('products.csv')
	intimates_products = pd_products.loc[pd_products['SubCategory'] == 'Intimates']

	for product_id in range(1, intimates_products.shape[0]):
		product = intimates_products.iloc[product_id]
		product_info = {}
		product_url = product['URL_to_product'].replace("///", "//www.zaful.com/")

		# req = Request(url=product_url, headers = headers)
		driver.get(product_url)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		sleep(3)
		soup = BeautifulSoup(driver.page_source, 'html.parser')
		description = soup.find("div", {"class": "xxkkk"})
		thumb_images = soup.find("div", {"class": "img-thumb"})
		thumb_images_url = thumb_images.find_all('img', )
		thumb_image_urls = [image['src'] for image in thumb_images_url]
		thumbail_color_p = soup.find("p", {"class": "active"})
		thumbail_color = thumbail_color_p.find("img", )['src']
		product_info['product_name'] = str(product['Name'])
		product_info['uniq_id'] = str(product['SKU'])
		product_info['description'] = str(description)
		product_info['price'] = "$" + str(product['Retail_Price'])
		product_info['product_imageurl'] = thumb_image_urls
		product_info['brand_name'] = "Zaful"
		product_info['available_size'] = [product['Size']]
		product_info['color'] = product['Color']
		product_info['color_thumbnail'] = thumbail_color
		product_info['product_category'] = "Lingerie"
		product_info['style_attributes'] = "Intimates"
		product_info['pageurl'] = str(product_url)

		all_products.append(product_info)
		total_product_number = total_product_number + 1
		# print("price", product_info['price'])
		print("zafu scraped product number", total_product_number)
		
	all_products = sorted(all_products, key=lambda x : x['color'], reverse=True)
	with open('static/victoria_secret.json', 'w') as outfile:
		json.dump(all_products, outfile)
	driver.quit()

# zaful_scraper()
