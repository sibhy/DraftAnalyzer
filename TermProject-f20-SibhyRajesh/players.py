## Sibhy Rajesh
## Term Project 15-112

## This file breaks down all csv data into a more easily accessible structure
## it also defines our fScore which we use to rank players

import pandas as pd

data = pd.read_csv("2019-fantasy-Data.csv")

# scoringOptions not used right now
scoringOptions = {
    "ydsMult":0.1, "passYdsMult":0.025, "ppr": 1.0, "int": -2,
    "tds": 6, "passTds": 4, "fmb": -2
}

# general class of players, includes name, team, age, etc;
class Player(object):

    allPlayers = []
    def __init__(self, name, team, age, pos, fpts):
        self.name = name.strip()
        self.team = team
        self.age = age
        self.pos = pos
        self.fpts = fpts
        self.fScore = 0
        self.scarcityCorrection = 1

    def  __repr__(self):
        spaceIndex = self.name.find(" ")
        return f"{self.name[0]}. {self.name[spaceIndex + 1:]}"

    def getfScore(self):
        return self.fScore

    # wrote the lt and gt methods for this class myself, but learned about them 
    # from here https://www.tutorialspoint.com/How-to-implement-Python-lt-gt-custom-overloaded-operators

    def __lt__(self, other):
        if isinstance(other, Player):
            return self.fScore < other.fScore
        elif isinstance(other, int) or isinstance(other, float):
            return self.fScore < other
        return False
    
    def __gt__(self, other):
        if isinstance(other, Player):
            return self.fScore > other.fScore
        elif isinstance(other, int) or isinstance(other, float):
            return self.fScore > other
        return False


# wide receivers are a type of player, do mostly receiving work
class wideReceiver(Player):
    def __init__(self, row):
        super().__init__(row['Player'], row['Tm'], row['Age'], row['FantPos'],
         row['PPR'])
        self.tgts = row['Tgt']
        self.rec = row['Rec']
        self.recYds = row['recYds']
        self.yr = row['Y/R']
        self.recTds = row['recTds']
        self.fmb = row['Fmb']
        self.fScore = self.receiverScore()
        self.scarcityCorrection = 1 # there are more available wrs than rbs
        
    # def __repr__(self):
    #     return f"{self.pos}: {self.name}"

    # convert a player's stats into an overall score
    def receiverScore(self):
        if self.rec == 0:
            self.fScore = 0
            return 0

        hands = self.rec/self.tgts
        volumeBonus = self.tgts
        rzUpside = self.recTds
        fScore = ((volumeBonus + hands + rzUpside - self.fmb)*
        self.scarcityCorrection)
        return fScore
    
# running backs can do receiving work, so make them a subset of receivers.
class runningBack(wideReceiver):

    def __init__(self, row):
        super().__init__(row)
        self.rushYds = row['rushYds']
        self.rushAtt = row['rushAtt']
        self.ya = row['Y/A']
        self.rushTds = row['rushTds']
        self.fScore += self.rushingScore()
     
    def rushingScore(self):
        rushPts = self.rushYds * 0.1
        volumeBonus = self.rushAtt * 0.01
        efficiency = self.ya
        rzUpside = self.rushTds
        scarcityCorrection = 1.5
        return (rushPts + volumeBonus*efficiency + rzUpside)*scarcityCorrection
        
# quarterbacks do passing work and rushing work
class quarterBack(runningBack):

    def __init__(self, row):
        super().__init__(row)
        self.cmp = row['Cmp']
        self.att = row['Att']
        self.passYds = row['Yds']
        self.passTds = row['TD']
        self.ints = row['Int']
        self.scarcityCorrection = 0.4 # lots of viable qbs available
        self.fScore += self.quarterbackScore()
        self.fScore += self.rushingScore() * 0.5 #

    def quarterbackScore(self):
        if self.att == 0:
            self.fScore = 0
            return 0
        eff = self.cmp/self.att
        volumeBonus = self.att
        rzUpside = self.passTds
        turnovers = self.ints
        passPts = self.passYds*0.025
        return (eff + passPts + rzUpside - turnovers)*self.scarcityCorrection


# tight ends are primarily for receiving in fantasy, so subclass of receiver
class tightEnd(wideReceiver):
    
    def __init__(self, row):
        super().__init__(row)
        self.scarcityCorrection = 1.75
        self.fScore *= self.scarcityCorrection

def createPlayers():
    for index, row in data.iterrows(): # this single line from: https://datascienceparichay.com/article/pandas-iterate-over-rows-of-a-dataframe/
        currPlayer = None
        if not isinstance(row['FantPos'], str): 
            continue
        if str(row['FantPos']).lower() == 'rb':
            currPlayer = runningBack(row)
        elif str(row['FantPos']).lower() == 'qb':
            currPlayer = quarterBack(row)
        elif str(row['FantPos']).lower() == 'wr':
            currPlayer = wideReceiver(row)
        elif str(row['FantPos']).lower() == 'te':
            currPlayer = tightEnd(row)
        if currPlayer != None:
            Player.allPlayers.append(currPlayer)


createPlayers()

sortedbyfScore = sorted(Player.allPlayers,key = Player.getfScore,reverse = True)
Player.allPlayers = sortedbyfScore




