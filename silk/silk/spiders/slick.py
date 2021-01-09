import scrapy
from scrapy_selenium import SeleniumRequest


class SlickSpider(scrapy.Spider):
    name = 'slick'

    def start_requests(self):
        yield SeleniumRequest(
            url='https://slickdeals.net/computer-deals/',
            wait_time=3,
            callback=self.parse

        )

    def parse(self, response):
        products = response.xpath("//ul[@class='dealTiles categoryGridDeals']/li")
        for product in products:

            yield {
                'name': product.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']/text()").get(),
                'link': product.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']/@href").get(),
                'price': product.xpath("normalize-space(.//div[@class='itemPrice  wide ']/text())").get(),
                'store': product.xpath(".//span[@class='blueprint']/button/text()").get(),
                'store_alrternative': product.xpath(".//span[@class='blueprint']/a/text()").get()
            }
        next_page = response.xpath("//a[@data-role='next-page']/@href").get()
        if next_page:
            absolute = f"https://slickdeals.net{next_page}"
            yield SeleniumRequest(
                url = absolute,
                wait_time=3,
                callback=self.parse
            )