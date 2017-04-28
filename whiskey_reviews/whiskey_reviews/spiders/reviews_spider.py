import scrapy


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    start_urls = [
        'https://www.connosr.com/whisky-reviews:1',
    ]

    def parse(self, response):
        for review in response.css('div.details'):
            yield {
                'source': "Connosr",
                'category': "Whiskey",
                'author': review.css('span.username::text').extract_first(),
                'product': review.css('span.product::text').extract_first(),
                'review': review.css('div.snippet p::text').extract_first(),
                'rating': review.css('span.score-circle::text').extract_first(),
                'likes': review.css('p.meta span.actions span.action.do-like i.value::text').extract_first(),
            }

        next_page = response.css('a.pagination-next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
