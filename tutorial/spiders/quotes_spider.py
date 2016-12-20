import scrapy
from tutorial.items import QuotesItem, AuthorItem
import logging


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ['toscrape.com']
    start_urls = [
            'http://quotes.toscrape.com',
        ]

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        #items = []
        for quote in response.css('div.quote'):
            item = QuotesItem()
            item['quote'] = quote.css('span.text::text').re(r'“(.*)”')[0]
            item['author'] = quote.css('span small::text').extract_first()
            item['tags'] = ', '.join(quote.css('div.tags a.tag::text').extract())
            yield item
            print(item['quote'])
            #items.append(item)


        for href in response.css('.author+a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_author)

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_author(self, response):
        self.logger.info('Parse function called on %s', response.url)
        item = AuthorItem()
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        item['name'] = extract_with_css('h3.author-title::text')
        item['birthdate'] = extract_with_css('span.author-born-date::text')
        item['location'] = extract_with_css('span.author-born-location::text')
        item['location'] = item['location'][3:len(item['location'])]
        item['description'] = extract_with_css('div.author-description::text')
        yield item
