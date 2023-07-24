import requests
from bs4 import BeautifulSoup
from database import MongoConnection
import math


class ScrapperNotFoundException(Exception):
    def __init__(self, scrapper_name: str) -> None:
        super().__init__("There is no such scrapper defined ", scrapper_name)


class Scrappers:

    class KitapyurduScrapper:

        def find(self, scrapper):
            # The function that finds the all related books and their needed attributes.
            self.books = []
            print(len(scrapper.words))

            for word in scrapper.words:

                page = 1
                is_finished = False
                response = requests.get(scrapper.url + f'index.php?route=product/search&filter_name={word}&fuzzy=0&filter_in_stock=1')
                last_page = 1

                while not is_finished:
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, "html.parser")

                        remove_content = soup.find('div', 'box gray no-padding ribbon-enable searched-products')
                        remove_content.decompose()

                        product_tags = soup.select(".product-cr")
                        pagination_tag = soup.select_one(".pagination")

                        if pagination_tag == None: break
                        
                        for product_tag in product_tags:
                            # title
                            title = product_tag.find("div", "name").find('span').text.strip()
                            # publisher
                            publisher = product_tag.find("div", "publisher").span.a.span.text.strip()
                            # writers                            
                            writers = product_tag.find_all("div", "author compact ellipsis", recursive=False)
                            writers = [writer.a.text.strip() for writer in writers]
                            # price
                            product_price = product_tag.find("div", "price-new").find("span", "value").text
                            product_price = product_price.strip().replace(',', '.')
                            price = float(product_price)

                            self.books.append(
                                {
                                    "title": title,
                                    "publisher": publisher,
                                    "writers": writers,
                                    "price": price,
                                }
                            )

                        last_page = int(pagination_tag.find("div", "results").text.split('(')[-1].split(' ')[0])

                        # Next page.
                        next_page = pagination_tag.find("a", "next")
                        if next_page != None:
                            next_page_href = next_page.get('href')
                            response = requests.get(next_page_href)

                    if page >= last_page:
                        is_finished = True
                    page += 1
            
        def save(self):
            if len(self.books) == 0:
                return
            else:
                conn = MongoConnection()
                collection_name = self.__class__.__name__.split("Scrapper")[0]
                collection_name = collection_name[0].lower() + collection_name[1:]
                conn.add_books(self.books, collection_name)
                conn.close_connection()

            
    class KitapsepetiScrapper:

        def find(self, scrapper):
            self.books = []

            for word in scrapper.words:

                page = 1
                is_finished = False

                response = requests.get(scrapper.url + f'arama?q={word}&stock=1')
                page_soup = BeautifulSoup(response.content, "html.parser")
                last_page = page_soup.find("span", "text-custom-dark-gray box double fl forDesktop").text.strip().split(" ")[2]
                last_page = math.ceil(int(last_page) / 60)

                while not is_finished:
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, "html.parser")

                        product_tags = soup.select(".productItem")
                        pagination_tag = soup.select_one(".productPager")

                        
                        if pagination_tag == None: break
                        
                        for product_tag in product_tags:
                            product_info = product_tag.find("div", "col col-12 productDetails loaderWrapper")
                            # title 
                            title = product_info.find("a", "fl col-12 text-description detailLink").text.strip()
                            # publisher
                            publisher = product_info.find("a", "col col-12 text-title mt").text.strip()
                            # writers
                            writers = [product_info.find("a", "fl col-12 text-title").text.strip()]
                            # price
                            product_price = product_tag.find("div", "currentPrice").text.strip().split('\n')[0].replace(',', '.')
                            price = float(product_price)
                            # print('price', price)

                            self.books.append(
                                {
                                    "title": title,
                                    "publisher": publisher,
                                    "writers": writers,
                                    "price": price
                                }
                            )


                        # Next page.
                        next_page = pagination_tag.find("a", "next")
                        if next_page != None:
                            next_page_href = next_page.get('href')
                            response = requests.get(next_page_href)

                    if page == last_page:
                        is_finished = True
                    page += 1

        def save(self):
            if len(self.books) == 0:
                return
            else:
                conn = MongoConnection()
                collection_name = self.__class__.__name__.split("Scrapper")[0]
                collection_name = collection_name[0].lower() + collection_name[1:]
                conn.add_books(self.books, collection_name)
                conn.close_connection()


class Scrapper:

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        if self.name == None:
            raise ScrapperNotFoundException(self.name)
        
        inner_scrapper = f'{self.name.capitalize()}Scrapper'
        self.inner_scrapper = getattr(Scrappers, inner_scrapper)()

        self.words = kwargs.get('words')
        self.url = kwargs.get('url')

    def operate(self):
        self.inner_scrapper.find(scrapper=self)
        self.inner_scrapper.save()