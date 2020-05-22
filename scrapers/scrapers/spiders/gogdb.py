"""Collect data from gogdb.org"""
import scrapy
from scrapers.items import GOGProduct

class GogdbSpider(scrapy.Spider):
    """"Spider for gogdb.org"""
    name = 'gogdb'
    allowed_domains = ['gogdb.org']
    start_urls = ['http://gogdb.org/products']
    # start_urls = ["https://www.gogdb.org/product/1531168671"]

    def parse(self, response):
        """Extract data from game list and pagination links"""
        for url in response.css("#product-table a::attr('href')"):
            full_url = response.urljoin(url.extract())
            yield scrapy.Request(full_url, callback=self.parse_product_page)
        for url in response.css(".pagination-container > a::attr('href')"):
            full_url = response.urljoin(url.extract())
            yield scrapy.Request(full_url, callback=self.parse)

    def parse_product_page(self, response):
        """Parser for a product page"""
        item = GOGProduct()
        item["url"] = response.url
        item["name"] = response.css("#page > h1::text").extract_first()
        for row in response.css("#info-table tr"):
            row_data = row.css("td::text").extract()
            if row_data[0] == "Supported Sytems":
                system_classes = ",".join(
                    system.replace("fa", "").strip("- ")
                    for system in row.css("i::attr('class')").extract()
                )
                row_data = ["Supported Systems", system_classes]
            item[row_data[0].lower().replace(" ", "_")] = row_data[1]
        return item
