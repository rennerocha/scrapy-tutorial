import scrapy


class HackerspaceListSpider(scrapy.Spider):
    name = 'hackerspace-list'
    start_urls = [
        'https://wiki.hackerspaces.org/'
        'List_of_ALL_Hacker_Spaces',
    ]

    def parse(self, response):
        for row in response.css('table tr'):
            yield {
                'hackerspace': row.css('.Hackerspace *::text').get(),
                'country': row.css('.Country *::text').get(),
                'status': row.css('.Hackerspace-status *::text').get(),
                'url': row.css('.Website a::attr(href)').get()
            }

        further_results = response.xpath(
            '//a[contains(text(), "further")]//@href|'
            '//a[contains(text(), "Next")]//@href')
        if further_results:
            yield scrapy.Request(response.urljoin(further_results.get()))
