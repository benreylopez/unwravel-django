from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome('chromedriver')
url = 'https://www.victoriassecret.com/vs/panties/bikinis'
driver.get(url)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(3)
soup = BeautifulSoup(driver.page_source, 'html.parser')

articles = soup.find_all('article', {'class': 'product-card-wrapper'})
print(len(articles))

for art in articles:
    img_url = art.find('img',)['src']
    print('https://www.victoriassecret.com'+img_url)

driver.quit()