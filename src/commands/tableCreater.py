import boto3 

dynamodb = boto3.resource('dynamodb')

def tableCreate(tableName):
# Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName=tableName,
        KeySchema=[
            {
                'AttributeName': "teamId",
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': "teamId",
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("created table "+tableName)
    return table

