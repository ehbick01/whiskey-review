from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', 
    region_name='us-east-1',
    aws_access_key_id = 'AKIAJTNL33WBCK5CFHQA',
    aws_secret_access_key = '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')

table = dynamodb.create_table(
    TableName='ConnosrReviews',
    KeySchema=[
        {
            'AttributeName': 'product',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'review',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'product',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'review',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)
