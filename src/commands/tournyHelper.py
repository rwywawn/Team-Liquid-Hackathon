import discord
import random
from tableCreater import tableCreate
from inputData import inputData
from queryData import queeryData

class Team():
    def __init__(self, name, round, id):
        self.name=name
        self.id=id
        self.round=round
        

class tournament ():

    def __init__(self, teams, name):
        self.teams = teams
        self.name = name
        # self.pairs=[]
        # self._last_member = None
        tableCreate(name)
        initialTeams()
        tournyData = {"round":self.round, "teamId":0, "teamName":"Tourny Data"}
        inputData(self.name, [tournyData])

    def update(winner, loser):
        #make database call, rounds number, games left, 


    def initialTeams():
        for i, team in enumerate(self.teams):
            self.teams.append(Team(team,1,i))

        inputData(self.name, self.teams)

    def createMatches():
        data = self.retrieve(id)
        round = data.round
        if ("matches in previous round are not done"):
            return "games not completed"

        round+=1
        teams=[]
        for i in data.teams:
            if i.round=round:
                teams.append(i)
        #update teams, update round info, 

    def retrieve(id):
        #retrieve data 
        return data