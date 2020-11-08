import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
dynamodb = boto3.resource('dynamodb')

def queryTeamsByID(tourny, teamID):
    table = dynamodb.Table(tourny)
    response = table.query(
        KeyConditionExpression=Key('teamId').eq(teamID)
    )
    return response['Items']
    
def queryTeamsByRound(tourny, round):
    table = dynamodb.Table(tourny)
    response = table.scan(FilterExpression=Key('round').eq(round))
    return response['Items']

def updateTeamByID(tourny, teamID):
    table = dynamodb.Table(tourny)
    response = table.update_item(
        Key={'teamId': teamID},
        UpdateExpression="set round = round + :val",
        ExpressionAttributeValues={
            ':val': Decimal(1),
        },
        ReturnValues="UPDATED_NEW"
    )
