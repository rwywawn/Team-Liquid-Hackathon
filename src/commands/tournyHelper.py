import discord
import random
from tableCreater import tableCreate
from 

class Team(name,round,id):
    def __init__(self,name,round):
        self.name=name
        self.id=id
        self.round=round
        

class tournament (teams, name):
    def __init__(self, teams, name):
        self.teams=[]
        self.name=name
        self.pairs=[]
        self._last_member = None
        tableCreate(name)
        initialTeams(teams)
        tournyData={"round":1,
        "teamId"=0,"teamName"="Tourny Data"}
        inputData(Item=tournyData)

    def update(winner,loser):
        #make database call, rounds number, games left, 

    def initialTeams(teams):
        id=0
        for i in teams:
            id+=1
            self.teams.append(Team(i,1,id))
        inputData(self.team, teams)

    def createMatches():
        data=self.retrieve(id)
        round=data.round
        if ("matches in previous round are not done"):
            return "games not completed"
        round+=1
        teams=[]
        for i in data.teams:
            if i.round=round:
                teams.append(i)
        #update teams, update round info, 

    def retrieve( id):
        #retrieve data 
        return data