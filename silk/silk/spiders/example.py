import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector


class ExampleSpider(scrapy.Spider):
    name = 'example'

    def start_requests(self):
        yield SeleniumRequest(
            url='https://duckduckgo.com',
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        img = response.request.meta['screenshot']
        with open('screenshot.png', 'wb') as f:
            f.write(img)
        driver = response.meta['driver']
        search = driver.find_element_by_xpath("//input[@id='search_form_input_homepage']")
        search.send_keys('Silk deals')
        driver.save_screenshot('after_input.png')
        search.send_keys(Keys.ENTER)
        driver.save_screenshot('afterenter.png')

        html = driver.page_source
        response_obj = Selector(text=html)
        links = response_obj.xpath("//div[@class='result__extras__url']/a")
        for link in links:
            yield {
                'url': link.xpath(".//@href").get()
            }
