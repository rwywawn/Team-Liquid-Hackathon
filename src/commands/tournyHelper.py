import discord
import random
from tableCreater import tableCreate
from inputData import inputData
from botocore.exceptions import ClientError
import boto3
import time
from queryData import queryTeamsByID, queryTeamsByRound, updateTeamByID

class tournament():

    def __init__(self, teamNames, name):
        self.teams = []
        self.rounds = [[]]
        self.current_round = 1
        for i, n in enumerate(teamNames):
            team = {}
            team["teamName"] = n
            team["round"] = 1
            team["teamId"] = i
            self.teams.append(team)
            self.rounds[0].append(team)
        
        if len(teamNames) % 2 != 0: 
            self.teams[0]["round"] = 2
            self.rounds.append([])
            self.rounds[1].append(self.teams[0])

        self.name = name
        dynamodb = boto3.resource('dynamodb')
        print(self.name)
        tableCreate(self.name)
        table = dynamodb.Table(self.name)
        table.meta.client.get_waiter('table_exists').wait(TableName=self.name)
        inputData(self.name, self.teams)
        tournyData = {"round":self.current_round, "teamId":100, "teamName":"TournyData"}
        inputData(self.name, [tournyData])

    def update(self, winner):
        #make database call, rounds number, games left, 
        teamId = None
        for team in self.teams:
            if team["teamName"] == winner:
                updateTeamByID(self.name, team["teamId"])
                team["round"] += 1
                if len(self.rounds) < team["round"]:
                    self.rounds.append([])

                self.rounds[team["round"]-1].append(team)
                if len(self.rounds[team["round"]-1]) == len(self.rounds[team["round"]-2])/2:
                    self.current_round += 1
                    updateTeamByID(self.name, 100)

                    if len(self.rounds[team["round"]-1]) % 2 != 0:
                        self.rounds.append([self.rounds[team["round"]-2][0]])

    def getCurrentRound(self):
        return self.current_round

    def getMatches(self): # show games for the current round
        result = []
        length = len(self.rounds[self.current_round-1])
        if length % 2 == 0:
            for i in range(0, length, 2):
                result.append([self.rounds[self.current_round-1][i]["teamName"], self.rounds[self.current_round-1][i+1]["teamName"]])

        else:
            for i in range(1, length, 2):
                result.append([self.rounds[self.current_round-1][i]["teamName"], self.rounds[self.current_round-1][i+1]["teamName"]])
            
        return result

    def getResults(self):
        pass
