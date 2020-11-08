import boto3
dynamodb = boto3.resource('dynamodb')


def inputData(tourny, teams):
    table = dynamodb.Table(tourny)
    for team in teams:
        print("inserting "+team["teamName"])
        table.put_item(Item=team)

    print("items inserted")

# inputData("ROCK",[{"round":1,"teamId":1,"teamName":"Poggers"},
# {"round":1,"teamId":2,"teamName":"Poggers"},
# {"round":1,"teamId":3,"teamName":"Poggers"},
# {"round":1,"teamId":4,"teamName":"Poggers"},
# {"round":1,"teamId":5,"teamName":"Poggers"},
# {"round":1,"teamId":6,"teamName":"Poggers"},
# {"round":1,"teamId":7,"teamName":"Poggers"},
# {"round":1,"teamId":8,"teamName":"Poggers"}])