import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')

def queryTeamsOnRound(tourny, round):

    table = dynamodb.Table(tourny)
    response = table.query(
        KeyConditionExpression=Key('round').eq(round)
    )
    print(response['Items'])
    return response['Items']

def queryTeamsByID(tourny, teamID, round):
    table = dynamodb.Table(tourny)
    response = table.query(
        KeyConditionExpression=
            Key('round').eq(round) & Key('teamId')
    )
    return resopnse['Items']
    