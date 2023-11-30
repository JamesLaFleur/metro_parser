import math
from bs4 import BeautifulSoup
import requests

URL = 'https://online.metro-cc.ru/category/bakaleya/krupy-bobovye'
PRODUCT_URL = 'https://online.metro-cc.ru'

PRODUCT_CARD_SELECTOR = '.product-card:not(.is-out-of-stock)'

BRAND_SELECTOR = '.product-attributes__list li:last-child'
ARTICLE_SELECTOR = '.product-page-content__article'
NAME_SELECTOR = 'product-card-name'
LINK_SELECTOR = 'product-card-photo__link'

PRICE_WRAPPER_SELECTOR = 'product-unit-prices__old-wrapper'
PRICE_WRAPPER_NEW_SELECTOR = 'product-unit-prices__actual-wrapper'
PRICE_SELECTOR = 'product-price__sum-rubles'

headers = {
    "User-Agent": 
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)"
}

jar = requests.cookies.RequestsCookieJar()
jar.set('UserSettings', 'SelectedStore=ddfaed10-5e08-458f-9967-baa9b63bd52e', domain='.metro-cc.ru', path='/')

def parseData(url: str) -> list[dict[str, str]]:
    print('Parse data started')
    html_text = requests.get(url, headers=headers, cookies=jar).text
    soup = BeautifulSoup(html_text, 'lxml')

    products_count_text = soup.select('.heading-products-count')[0]
    products_count = int(products_count_text.text.split()[0])
    pages_count = math.ceil(products_count / 30) 

    for page in range(1, pages_count+1):
        print('START PARSE FOR PAGE: ', page)
        if(page == 1):
            yield parseProductsInfo(soup)
        else:
            yield parseProductsInfo(getPageData(url, page))


def getPageData(url: str, page: int) -> BeautifulSoup:
    html_text = requests.get(url + '?page=' + str(page), headers=headers, cookies=jar).text
    return BeautifulSoup(html_text, 'lxml')


def parseProductsInfo(soupEx: BeautifulSoup) -> list[dict[str, str]]:
    products_in_stock = soupEx.select(PRODUCT_CARD_SELECTOR)

    result = []

    for product in products_in_stock:
        product_name = product.find('a',  class_ = NAME_SELECTOR).text.strip()
        product_act_price = product.find('div', class_ = PRICE_WRAPPER_NEW_SELECTOR).find('span', class_ = PRICE_SELECTOR).text
        product_old_price = product.find('div', class_ = PRICE_WRAPPER_SELECTOR).find('span', class_ = PRICE_SELECTOR)
        
        product_link = PRODUCT_URL + product.find('a', class_ = LINK_SELECTOR).get('href')
        

        prod_info = requests.get(product_link, headers=headers).text
        soup = BeautifulSoup(prod_info, 'lxml')

        product_id_container = soup.select(ARTICLE_SELECTOR)
        product_id = product_id_container[0].text.split()[1] if product_id_container else '--'
        product_info_items = soup.select(BRAND_SELECTOR)

        for item in product_info_items:
            if "Бренд" in item.text:
                link = item.find('a')
                if link: 
                    brand_name = item.find('a').text.strip()


        data = {
            'ProductID': product_id,
            'Product_name': product_name,
            'Actual_price':product_act_price,
            'Old_price': product_old_price.text if product_old_price else '--',
            'Product_link': product_link,
            'Brand': brand_name,
        }

        result.append(data)

    return result