import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')

def query_movies(tourny,round):

    table = dynamodb.Table(tourny)
    response = table.query(
        KeyConditionExpression=Key('round').eq(round)
    )
    print(response['Items'])
    return response['Items']
