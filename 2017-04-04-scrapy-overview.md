Scraping Whiskey Reviews Using Scrapy
===

## Background
This is a working document to help understand the first stage of this project - the data grab. It is also a helpful learning tool for myself, as this is the first **real** spider that I've created to pull data from a website.

## Setup
The initial setup is quick, simply `cd` into the directory that you want to work in and run - 

```
scrapy startproject whiskey_reviews
```
Easy enough. 

## Initial file structure
The above command builds out the following file structure:

```
whiskey_reviews
|-- whiskey_reviews
	|-- spiders
		|--__init__.py
	|-- __init__.py
	|-- items.py
	|-- middlewares.py	
	|-- pipelines.py
	|-- settings.py
|-- scrapy.cfg
```
**File descriptors**
To understand the infrascture that's been built, let's break down the files and filepaths and what they are doing

*/whiskey_reviews*

| File        | Description  |
| :-------------|:---------|
| */whiskey_reviews* | Project's Python module where code will be imported from |
| `scrapy.cfg` | Deployment configuration file |

*/whiskey_reviews/whiskey_reviews*

| File        | Description  |
| :-------------|:---------|
| */spiders* | Directory for spiders to be placed |
| `__init__.py` | Marks package directory for project |
| `items.py` | Project items definition file |
| `middlewares.py` | Project middlewares to alter request/responses |
| `pipelines.py` | Project pipelines file |
| `settings.py` | Project settings file |

*/whiskey_reviews/spiders*

| File        | Description  |
| :-------------|:---------|
| `__init__.py` | Marks package directory for spiders |

At the very start of this, we will not be messing with the `pipelines.py` file - but once we have a dedicated db set up we will likely tweak those settings as well. Until then, all results will be stored as JSON files.

## What's the data I'm grabbing?
For this project, I am scraping whiskey product reviews from [this site](http://wwwconnosr.com/). In particular, for each review I am grabbing the following: 

- Author
- Product
- Review
- Rating
- Likes given for the review

## What am I doing with it?
Aside from just learning how to do this whole thing, I am going to use the data to tune a learner against, and feed the results of that work into a recommender that is hosted on an app. This will not only give me insights on how to build these spiders, but also how to store their results and use the data for modeling - and then to develop the infrastructure to deliver the output in a meaningful way. 

## Workflow

**Step 1 - Create spider**

[My spider](whiskey_reviews/whiskey_reviews/spiders/reviews_spider.py) is structurally similar to the tutorial version hosted on the `scrapy` doc site. 

```
import scrapy


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    start_urls = [
        'https://www.connosr.com/whisky-reviews:1',
    ]

    def parse(self, response):
        for review in response.css('div.details'):
            yield {
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
``` 

There are three main components of this script. The first - 

```
class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    start_urls = [
        'https://www.connosr.com/whisky-reviews:1',
    ]
```

Defines the spider's name that we will build and the URL starting point - `https://www.connosr.com/whiskey-reviews:1` that the spider will begin at.

The second component - 

```
def parse(self, response):
    for review in response.css('div.details'):
        yield {
            'author': review.css('span.username::text').extract_first(),
            'product': review.css('span.product::text').extract_first(),
            'review': review.css('div.snippet p::text').extract_first(),
            'rating': review.css('span.score-circle::text').extract_first(),
            'likes': review.css('p.meta span.actions span.action.do-like i.value::text').extract_first(),
        }
```

Creates the `parse()` function that will be applied to each request. In this case, our scraper will find the `details` class of the `<div>` element - and from within that block, pulls our relevant information based on the their HTML paths.

For instance, the author's name is stored in the `username` class of the `<span>` element beneath `div.details` - which is reflected in the selector path for the author variable that we are collecting.

The final component - 

```
next_page = response.css('a.pagination-next::attr(href)').extract_first()
if next_page is not None:
    next_page = response.urljoin(next_page)
    yield scrapy.Request(next_page, callback=self.parse)
```

Defines the recursive parsing of pages. This allows us to run our spider across all pages of the site, and automatically ends on the final page. 

**Step 2 - Running Spider**

`cd` into the main directory for the project - which is wherever the `scrapy.cfg` file exists. Once there, run -

```
scrapy crawl reviews -o reviews.json
```


**Step 3 - Storing Results**

The simplest way to store results from a spider is to either write them to JSON or JSON Lines format. The benefit of using JSON Lines is that you can run the scraper more than once without it crashing - and each record is a separate line so not everything is stored to memory.

For the sake of industry standardization, I am sticking with JSON format for crawling. Using JSON Lines may work for standalone side projects, but for anything open source JSON will likely be used.

**Step 4 - Productionalizing**

Eventually, these will be fed into either a `postgresql` or `dynamoDB` space. I haven't set those up, but once I do I will link to the overview for that section of the stack here. 