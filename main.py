from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

ZILLOW_URL = "https://www.zillow.com/los-angeles-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
             "%22mapBounds%22%3A%7B%22north%22%3A34.337306%2C%22east%22%3A-118.155289%2C%22south%22%3A33.703652%2" \
             "C%22west%22%3A-118.668176%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%" \
             "7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value" \
             "%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22" \
             "%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afal" \
             "se%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListV" \
             "isible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12447%2C%22regionType%22%3A6%7D%5D%7D"
ZILLOW_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/107.0.0.0 Safari/537.36",
    "Accept-Language": "es-419,es;q=0.9"
}
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfC1eKCfaR2mACyPT_WsrELyVSSKB2ZcQ5KTGarbWwZkU-KWQ/" \
                  "viewform?usp=sf_link"
CHROME_DRIVER_PATH = Service("C:\Development\chromedriver.exe")


#TODO 1 scrape the listing of the zillow web address
    #TODO 1.1 make the request
response = requests.get(url=ZILLOW_URL, headers=ZILLOW_HEADERS)
response.raise_for_status()
data = response.text
    #TODO 1.2 create the BeautifulSoup object
bs = BeautifulSoup(data, "html.parser")

#TODO 2 make three lists with the required data (price, address and link)
price_list_data = bs.select("span[data-test='property-card-price']")
price_list = [price.text[0:6] for price in price_list_data]
address_list_data = bs.select("address[data-test='property-card-addr']")
address_list = [address.text for address in address_list_data]
link_list_data = bs.select("a[data-test='property-card-link']")
link_list = [f"https://www.zillow.com/{link.get('href')}" for link in link_list_data]


#TODO 3 with selenium fill the google form with each house and refresh each time
driver = webdriver.Chrome(service=CHROME_DRIVER_PATH)
driver.get(GOOGLE_FORM_URL)
time.sleep(3)

for _ in range(len(price_list)):
    address_input = driver.find_element(By.CSS_SELECTOR, "input[aria-describedby='i2 i3']")
    price_input = driver.find_element(By.CSS_SELECTOR, "input[aria-describedby='i6 i7']")
    link_input = driver.find_element(By.CSS_SELECTOR, "input[aria-describedby='i10 i11']")
    send_button_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    time.sleep(2)
    address_input.send_keys(address_list[_])
    price_input.send_keys(price_list[_])
    link_input.send_keys(link_list[_])
    time.sleep(2)
    send_button_input.click()
    time.sleep(3)
    driver.refresh()
    time.sleep(3)
