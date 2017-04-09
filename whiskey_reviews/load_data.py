from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb', 
    region_name='us-east-1',
    aws_access_key_id = 'AKIAJTNL33WBCK5CFHQA',
    aws_secret_access_key = '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')

table = dynamodb.Table('ConnosrReviews')

with open("reviews.json") as json_file:
    reviews = json.load(json_file, parse_float = decimal.Decimal)
    for review in reviews:
        product = review['product']
        review = review['review']
        rating = int(review['rating'])
        likes = int(review['likes'])
        author = review['author']

        print("Adding review:", product, review)

        table.put_item(
           Item={
               'product': product,
               'review': review,
               'rating': rating,
               'likes': likes,
               'author': author,
            }
        )