import scrapy

class ConnosrFullSpider(scrapy.Spider):

    # Name of spider
    name = "connosr-comments"

    # Designed domains and starting URL
    allowed_domains = [
        'connosr.com'
        ]
    start_urls = [
        'https://www.connosr.com/whisky-reviews',
        ]

    # Define initial parsing function
    def parse(self, response):

        # follow links to product pages
        for site in response.css('div.details h3 a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(site),
                                 callback=self.parse_product)

        # Carry through to the next page until `a.pagination` no longer exists
        next_page = response.css('a.pagination-next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    # Define product parsing function
    def parse_product(self, response):

        # Define function to parse individual page info
        def extract_with_css(query):
            return response.css(query).extract_first()

        # Define function to parse whole review info
        def extract_review(query):
            return response.css(query).extract()

        # Define function to parse product meta data
        def extract_facts(query):
            return response.css(query).extract()

        # Yield page details
        yield {
            # Pull meta data
            'source': "Connosr",
            'type': extract_facts('div.facts li span.data a::text')[1],
            'author': extract_with_css('h2.wf-text span.username a::attr(href)'),

            # Pull product info
            'product': extract_with_css('header.details h1::text'),
            'brand': extract_facts('div.facts li span.data a::text')[0],
            # 'abv': extract_with_css('div.facts li span.data::text'),
            # 'taste-profile': extract_with_css('div.review-tags.tag-list ul li a::text'),

            # Pull user review info
            # 'review': extract_review('div.review-body p::text'),
            # 'nose-rating': extract_review('div.info li div::text')[0],
            # 'taste-rating': extract_review('div.info li div::text')[1],
            # 'finish-rating': extract_review('div.info li div::text')[2],
            # 'balance-rating': extract_review('div.info li div::text')[3],
            # 'overall-rating': extract_review('div.info li div::text')[4],
            'comment-authors': extract_review('article.comment div.author-content div.title a::text')
        }
