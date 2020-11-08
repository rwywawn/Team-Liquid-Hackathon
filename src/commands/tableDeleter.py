import boto3

def delete_movie_table(tableName):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(tableName)
    table.delete()
    print (tableName+"table deleted")
