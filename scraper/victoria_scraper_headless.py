from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import base64
import json
from collections import Counter

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

# API path
API_path = 'https://api.victoriassecret.com/products/v4/page/'

total_product_number = 0
all_products = []
def get_products(url):
	driver = webdriver.Chrome('chromedriver', options=opts)
	global total_product_number
	global all_products
	for i in range(1, 20):
		driver.get(url)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		sleep(3)
		soup = BeautifulSoup(driver.page_source, 'html.parser')

		articles = soup.find_all('article', {'class': 'product-card-wrapper'})
		if (len(articles) > 0):
			break

	for art in articles:
		product_info = {}
		# Extract uniq_id
		uniq_id = art['data-uuid']
		uniq_id_list = [product['uniq_id'] for product in all_products]
		if uniq_id in uniq_id_list:
			continue
		url_split = url.split('/')
		check_status = False
		# API_path for getting detailed product information
		product_api_path = API_path + uniq_id
		for check in range(1, 10):
			check_status, product_info = detailed_product_information(product_api_path)
			if check_status:
				break

		product_info['product_category'] = url_split[-2].capitalize()
		product_info['style_attributes'] = url_split[-1]

		img_url = art.find('a',)['href']
		# print('https://www.victoriassecret.com'+img_url)
		product_info['uniq_id'] = uniq_id
		product_info['pageurl'] = 'https://www.victoriassecret.com'+img_url

		# find price
		temp_price = art.find('p', {'class': 'price'})
		check_price = str(temp_price.text).split()[0]
		if check_price == "Original":
			check_price = str(temp_price.text).split()[3]
		product_info['price'] = check_price
		if check_status:
			total_product_number = total_product_number + 1
			print("total_product_number: ", total_product_number)
			all_products.append(product_info)
	driver.quit()

def detailed_product_information(product_api_path):
	check_status = False
	try:
		product_info = {}
		with urllib.request.urlopen(product_api_path) as response:
			detailed_information = response.read()
		detailed_information = detailed_information.decode('utf8')
		json_information = json.loads(detailed_information)
		product = json_information['product']
		product_info['product_name'] = product['shortDescription']
		product_info['brand_name'] = product['brandName']

		genericId = product['featuredChoice']['genericId']
		choice = product['featuredChoice']['choice']
		
		# get available sizes
		all_inventory = product['inventory']
		my_inventory = [inventory for inventory in all_inventory if ((inventory['genericId'] == genericId) and (inventory['choice'] == choice))]
		# price_info = my_inventory[0]
		# product_info['price'] = price_info['salePrice']

		sizes = []
		for inventory in my_inventory:
			size1 = inventory['size1']
			try:
				size2 = inventory['size2']
			except:
				size2 = ""
			size = size1 + size2
			print("size is : ", size)
			if size not in sizes:
				sizes.append(size)
		product_info['available_size'] = sizes
		
		# get Description
		longDescription = product['longDescription']
		mydescription = [description for description in longDescription if description['genericId'] == genericId]
		product_info['description'] = mydescription[0]['html']

		# get product images
		purchasableImages = product['purchasableImages']
		all_images = [image['choices'] for image in purchasableImages if image['genericId'] == genericId]
		myimages = all_images[0]
		myimages = [image['images'] for image in myimages if image['choice'] == choice]
		myimages = myimages[0]
		my_image_urls = []
		for image in myimages:
			my_image_url = "https://dm.victoriassecret.com/p/760x1013/" + image['image'] + ".jpg"
			my_image_urls.append(my_image_url)

		# get color
		selectors = product['selectors']['choice']
		all_colors = [selector['options'] for selector in selectors if selector['genericId'] == genericId]
		my_colors = all_colors[0]
		my_color = [color for color in my_colors if color['value'] == choice]
		my_color = my_color[0]
		product_info['color'] = my_color['label']
		product_info['color_thumbnail'] = "https://dm.victoriassecret.com/p/760x1013/" + my_color['image'] + ".jpg"

		product_info['product_imageurl'] = my_image_urls
		check_status = True
	except:
		check_status = False
	
	return check_status, product_info

def scraper():
	print("victoriassecret products scraping started ....")
	global total_product_number
	global all_products
	total_product_number = 0
	all_products = []
	url_list = [
	'https://www.victoriassecret.com/vs/bras/demi',
	'https://www.victoriassecret.com/vs/bras/full-coverage',
	'https://www.victoriassecret.com/vs/bras/perfect-shape',
	'https://www.victoriassecret.com/vs/bras/t-shirt-bra',
	'https://www.victoriassecret.com/vs/bras/lounge-and-wireless',
	'https://www.victoriassecret.com/vs/bras/strapless-and-backless',
	'https://www.victoriassecret.com/vs/bras/bralette',
	'https://www.victoriassecret.com/vs/bras/sports-bras',
	'https://www.victoriassecret.com/vs/bras/bra-accessories',
	'https://www.victoriassecret.com/vs/panties/thongs-and-v-strings',
	'https://www.victoriassecret.com/vs/panties/cheekies-and-cheekinis',
	'https://www.victoriassecret.com/vs/panties/brazilian-panties',
	'https://www.victoriassecret.com/vs/panties/bikinis',
	'https://www.victoriassecret.com/vs/panties/briefs',
	'https://www.victoriassecret.com/vs/panties/hiphuggers',
	'https://www.victoriassecret.com/vs/panties/boyshorts-shorties',
	'https://www.victoriassecret.com/vs/panties/high-waisted-panties',
	'https://www.victoriassecret.com/vs/panties/no-show-and-seamless',
	'https://www.victoriassecret.com/vs/panties/sports-underwear',
	'https://www.victoriassecret.com/vs/lingerie/teddies-and-bodysuits',
	'https://www.victoriassecret.com/vs/lingerie/babydolls',
	'https://www.victoriassecret.com/vs/lingerie/corsets-and-bustiers',
	'https://www.victoriassecret.com/vs/lingerie/corsets-and-bustiers',
	'https://www.victoriassecret.com/vs/lingerie/bras-and-panties',
	'https://www.victoriassecret.com/vs/lingerie/slips',
	'https://www.victoriassecret.com/vs/lingerie/kimonos',
	'https://www.victoriassecret.com/vs/sleepwear/tops',
	'https://www.victoriassecret.com/vs/sleepwear/pajama-shorts',
	'https://www.victoriassecret.com/vs/sleepwear/bottoms',
	'https://www.victoriassecret.com/vs/sleepwear/loungewear',
	'https://www.victoriassecret.com/vs/sleepwear/robes-and-slippers',
	'https://www.victoriassecret.com/vs/sleepwear/womens-slippers',
	'https://www.victoriassecret.com/vs/sleepwear/rompers-and-jumpsuits'
	"https://www.victoriassecret.com/pink/bras/bralette",
	"https://www.victoriassecret.com/pink/bras/sport-bras-collection",
	"https://www.victoriassecret.com/pink/bras/wireless-styles",
	"https://www.victoriassecret.com/pink/bras/push-up",
	"https://www.victoriassecret.com/pink/bras/lightly-lined",
	"https://www.victoriassecret.com/pink/bras/strapless",
	"https://www.victoriassecret.com/pink/panties/thongs",
	"https://www.victoriassecret.com/pink/panties/boyshorts",
	"https://www.victoriassecret.com/pink/panties/cheeksters",
	"https://www.victoriassecret.com/pink/panties/hipsters",
	"https://www.victoriassecret.com/pink/panties/bikinis"
	]
	product_path = "https://api.victoriassecret.com/products/v4/page/87ed8b77-6ff0-42d3-afb2-e1324e2712c4"
	for url in url_list:
		get_products(url)
	# detailed_product_information(product_path)
	with open('static/victoria_secret_temp.json', 'w') as outfile:
		json.dump(all_products, outfile)
	
# main()
scraper()
