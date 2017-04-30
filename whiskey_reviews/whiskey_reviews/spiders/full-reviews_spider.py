# Need to dig into each review link to pull more data
# To find all review links on each page
# -- response.css('div.details h3 a::attr(href)').extract()


import scrapy

class ConnosrFullSpider(scrapy.Spider):
    name = "connosr-full"
    allowed_domains = [
        'connosr.com']
    start_urls = [
        'https://www.connosr.com/whisky-reviews:1',
    ]

    def parse(self, response):
        # follow links to author pages
        for site in response.css('div.details h3 a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(site),
                                 callback=self.parse_product)

        next_page = response.css('a.pagination-next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_product(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()
        def extract_review(query):
            return response.css(query).extract()
        yield {
            'source': "Connosr",
            'category': "Whiskey",
            'author': extract_with_css('h2.wf-text span.username a::attr(href)'),
            'product': extract_with_css('header.details h1::text'),
            'review': extract_with_css('div.review-body p::text'),
            'rating': extract_review('div.info li div::text'),
            'likes': extract_with_css('i.value::text'),
        }
