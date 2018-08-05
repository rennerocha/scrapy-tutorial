# -*- coding: utf-8 -*-
import scrapy


class LoginQuotesSpider(scrapy.Spider):
    name = 'login_quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        form_data = {
            'username': 'username',
            'password': 'password',
            'csrf_token': csrf_token,
        }

        yield scrapy.FormRequest(
            response.url,
            formdata=form_data,
            callback=self.parse_logged_in,
        )

    def parse_logged_in(self, response):
        for quote in response.css('.quote'):
            yield {
                'quote': quote.css('.text::text').get(),
                'author': quote.css('.author::text').get(),
                'author_url': response.urljoin(
                    quote.xpath('.//a[contains(text(), "about")]/@href').get()),
                'tags': quote.css('.tag *::text').getall(),
            }

        yield scrapy.Request(
            response.urljoin(
                response.css('.next a::attr(href)').get()
            ),
            callback=self.parse_logged_in,
        )
