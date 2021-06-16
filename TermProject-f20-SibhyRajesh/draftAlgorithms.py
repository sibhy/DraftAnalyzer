## Sibhy Rajesh
## Term Project 15-112
from players import *
import copy

# this file includes various draft algorithms I've written for the term project

Player.allPlayers.sort(key = Player.getfScore, reverse = True)

# "Auto Draft"
# basic draft that pulls the best remaing player in the list of players.
# Pros: Tries to maximize total fScore. Get the most "bang for your buck"
# Cons: Doesn't guarantee a complete roster, might not have a te or qb for ex

def autoDraft(managers, players):
    rosterSize = 6
    rosters = [ [None for i in range(rosterSize)] for i in range(managers)]
    return autoDraftHelper(rosters, players, 0)

def autoDraftHelper(rosters, players, turn):
    if not autoDraftOver(rosters):
        rosters[turn % len(rosters)].insert(0, players[0])
        rosters[turn % len(rosters)].pop()
        return autoDraftHelper(rosters, players[1:], turn + 1)
    else:
        return rosters

def autoDraftOver(rosters):
    for roster in rosters:
        for player in roster:
            if player == None:
                return False
    return True

# print(autoDraft(12, Player.allPlayers))

# "Positional Draft"
# draft algorithm that prioritizes filling starting lineup positions
# can pass in the roster requirements as a parameter or use default
# Pros: Guarantees all roster positions are filled with the best avail player
# Cons: Could miss out on value based drafting due to strict positional req

def positionalDraft(numberOfPlayers, players, reqRoster = {"qb": 1, "wr": 2, "rb": 2, "te":1 }):
    defaultRoster = {"qb": set(), "wr": set(), "rb":set(), "te": set()}
    rosters = [copy.deepcopy(defaultRoster) for i in range(numberOfPlayers)]
    return positionalDraftHelper(rosters, players, 0, reqRoster)

def positionalDraftHelper(rosters, players, turn, reqRoster):
    if positionalDraftOver(rosters, reqRoster): 
        return rosters  
    
    prioritize = set()
    turn %= len(rosters)
    roster = rosters[turn]

    for pos in reqRoster:
        if reqRoster[pos] > len(roster[pos]):
            prioritize.add(pos) 
            
    for player in players:
        if player.pos.lower() in prioritize:
            rosters[turn][player.pos.lower()].add(player)
            index = players.index(player)
            currPlayers = players[:index] + players[index + 1:]
            break
    
    return positionalDraftHelper(rosters, currPlayers, turn + 1, reqRoster)
    
def positionalDraftOver(rosters, reqRoster):
    playersDrafted = 0
    for roster in rosters:
        playersDrafted += (len(roster["qb"]) + len(roster["wr"]) 
        + len(roster["rb"]) + len(roster["te"]))
    
    return playersDrafted == (len(rosters)*(reqRoster["qb"] + 
    reqRoster["wr"] + reqRoster["rb"] + reqRoster["te"]))

# print(positionalDraft(12,Player.allPlayers, {"qb": 1, "wr": 2, "rb": 2, "te":1}))

# Adversarial Draft
# functions similar to positional draft, but with one person manually drafting 
# and the rest AI. Also, the AI will target players that the manual drafter 
# needs to make it more difficult. 

def adversarialDraft(numberOfPlayers, players, manual, reqRoster =  {"qb": 1, "wr": 2, "rb": 2, "te":1}):
    defaultRoster = {"qb": set(), "wr": set(), "rb":set(), "te": set()}
    rosters = [copy.deepcopy(defaultRoster) for i in range(numberOfPlayers)]
    return adversarialDraftHelper(rosters, players, 0, reqRoster, manual)

def adversarialDraftHelper(rosters, players, turn, reqRoster, manual):
    if adversarialDraftOver(rosters, reqRoster): return rosters
    turn %= len(rosters)
    if turn == manual:
        rosters[turn][players[0].pos.lower()].add(players[0])
        players.pop(0)

        # manual drafting option, fully works- commented out for now, just use AI autodraft
        # playerNameList =  [player.name.lower() for player in players]
        # print("Suggested Players: ")
        # suggestedPlayers = getSuggestedPlayers(rosters[manual], players, 
        # rosters, reqRoster)
        # if suggestedPlayers != None:
        #     for player in suggestedPlayers:
        #         print(player.name)
        # else:
        #     print("None")
        # playerName = input("Enter Player Name to Draft Them:").lower()
        # playerIndex = playerNameList.index(playerName)
        # playerObj = players[playerIndex]
        # rosters[turn][playerObj.pos.lower()].add(playerObj)
        # players.remove(playerObj)

    else:
        prioritize = set()
        for pos in reqRoster:
            if reqRoster[pos] > len(rosters[manual][pos]):
                prioritize.add(pos)
        
        for player in players:
            if player.pos.lower() in prioritize:
                rosters[turn][player.pos.lower()].add(player)
                players.remove(player)
                break    

    return adversarialDraftHelper(rosters, players, turn + 1, reqRoster, manual)

def adversarialDraftOver(rosters, reqRoster):
    playersDrafted = 0
    for roster in rosters:
        playersDrafted += (len(roster["qb"]) + len(roster["wr"]) + len(roster["rb"]) + len(roster["te"]))
    return playersDrafted == (len(rosters)*(reqRoster["qb"] + 
    reqRoster["wr"] + reqRoster["rb"] + reqRoster["te"]))

# print(adversarialDraft(12, Player.allPlayers, 0))

# this function would suggest players from categories the player needs
def getSuggestedPlayers(roster, remainingPlayers, rosters, reqRoster = {"qb": 1, "wr": 2, "rb": 2, "te":1}):
    
    prioritize = set()
    for pos in reqRoster:
        if reqRoster[pos] > len(roster[pos]):
            prioritize.add(pos)
    
    suggestedPlayers = []
    
    i = 0
    playersAdded = 0
    while(playersAdded < len(rosters)):
        if i >= len(remainingPlayers):
            if suggestedPlayers == []:
                return remainingPlayers[:len(rosters) + 1]
            return suggestedPlayers
        player = remainingPlayers[i]
        if player.pos.lower() in prioritize:
            suggestedPlayers.append(player)
            playersAdded += 1
        i += 1
        player = None

    return suggestedPlayers
        
# print(adversarialDraft(12, Player.allPlayers))


###################
# Minimax w/ Snake(w/ alpha-beta pruning)
# the helper uses a list of moves which indicate the path taken by the 
# minimax function. We only need the first move from that path, and then 
# we keep calling minimax with our new updated roster to get the bestMove 
# from that point and adding it to our new rosters. Also added alpha-beta 
# pruning to make it more efficient. 
# currently adding: snake order, so instead of 1 2 1 2, goes 1 2 2 1 1 ...

# learned from: https://www.youtube.com/watch?v=KU9Ch59-4vw
# learned from and used a similar code structure to the one here: https://www.youtube.com/watch?v=l-hh51ncgDI
# this video linked the following code: https://pastebin.com/rZg1Mz9G
# used the same alpha-beta pruning implementation as this one: https://www.youtube.com/watch?v=l-hh51ncgDI

def minimaxDraft(numberOfRosters, players, snake, reqRoster = {"qb": 1, "wr": 2, "rb": 2, "te":1}):
    defaultRoster = {"qb": set(), "wr": set(), "rb":set(), "te": set()}
    rosters = [copy.deepcopy(defaultRoster) for i in range(numberOfRosters)]
    turn = 0
    depth = 3
    maxTurn = 0
    moveList = []
    realRosters = [copy.deepcopy(defaultRoster) for i in range(numberOfRosters)]
    alpha = -float('inf')
    beta = float('inf')
    turnIncrement = 1
    snakeDelay = 1

    while not minimaxDraftOver(rosters, reqRoster):
        
        bestAvailPlayer = minimaxDraftHelper(rosters, turn, players, depth, maxTurn, reqRoster, moveList, alpha, beta)[1][0]
        realRosters[turn][bestAvailPlayer.pos.lower()].add(bestAvailPlayer)
        
        # snake drafts go 1,2,2,1,1... instead of 1,2,1,2...
        if not snake:
            turn += turnIncrement
            turn %= len(realRosters)
        else:
            if turn == len(realRosters) - 1 and snakeDelay == 0:
                turnIncrement *= -1
                snakeDelay += 1
            elif turn == 0  and snakeDelay == 0:
                turnIncrement *= - 1
                snakeDelay += 1
            else:
                turn += turnIncrement
                snakeDelay = 0
            
        moveList = []
        rosters = copy.deepcopy(realRosters)
        players.remove(bestAvailPlayer)

    return realRosters

# helper will return the 'path' made by the mini and max players and the score
def minimaxDraftHelper(rosters, turn, remainingPlayers, depth, maxTurn, reqRoster, moveList, alpha, beta):

    turn %= len(rosters)
    # base case
    if depth == 0:
        return (evaluateRoster(rosters[maxTurn]), moveList)

    # if maximizing player turn, they try to get the best
    if turn == maxTurn:

        suggPlayers = getSuggestedPlayers(rosters[maxTurn], remainingPlayers,
        rosters, reqRoster) # these are possible moves

        maxRosterEval = -float('inf')

        for player in suggPlayers:
            tempRoster = rosters[maxTurn]
            tempRoster[player.pos.lower()].add(player)
            playerIndex = remainingPlayers.index(player)
            tempRemainingPlayers = remainingPlayers[:playerIndex] + remainingPlayers[playerIndex + 1:]
            # tempRosters = rosters[:maxTurn] + [tempRoster]

            rosters[maxTurn] = tempRoster
            moveList.append(player)

            tempEval = minimaxDraftHelper(rosters, turn + 1, tempRemainingPlayers, depth - 1, maxTurn, reqRoster, moveList, alpha, beta)
            maxRosterEval = max(maxRosterEval, tempEval[0])

            alpha = max(alpha, maxRosterEval) # from https://www.youtube.com/watch?v=l-hh51ncgDI
            if beta <= alpha:
                break

        return (maxRosterEval, moveList)

    else: 

        suggPlayers = getSuggestedPlayers(rosters[maxTurn], remainingPlayers, 
        rosters, reqRoster)

        minRosterEval = float('inf')

        for player in suggPlayers:
            tempRoster = rosters[turn] # temp roster we change
            tempRoster[player.pos.lower()].add(player) # add the player
            playerIndex = remainingPlayers.index(player) # to non-destructively remove from players
            tempRemainingPlayers = remainingPlayers[:playerIndex] + remainingPlayers[playerIndex + 1:]

            rosters[turn] = tempRoster # destructively changes roster

            moveList.append(player) # add this to our list of moves
            tempEval = minimaxDraftHelper(rosters, turn + 1, tempRemainingPlayers, depth - 1, maxTurn, reqRoster, moveList, alpha, beta)
            minRosterEval = min(minRosterEval, tempEval[0])

            beta = min(minRosterEval, beta) # like above, from https://www.youtube.com/watch?v=l-hh51ncgDI
            if beta <= alpha:
                break

        return (minRosterEval, moveList)

# heuristic function, when depth hits 0, we need to determine who the position 
# is better for. Will just return the total fScore of the current roster, 
# and the mini tries to choose the lower one, and max will try to get the higher one

def evaluateRoster(roster):
    totalFScore = 0
    
    for pos in roster:
        for player in roster[pos]:
            totalFScore += player.fScore

    return totalFScore

def minimaxDraftOver(rosters, reqRoster):
    playersDrafted = 0
    for roster in rosters:
        playersDrafted += (len(roster["qb"]) + len(roster["wr"]) + len(roster["rb"]) + len(roster["te"]))
    rosterTotal = (len(rosters)*(reqRoster["qb"] + 
    reqRoster["wr"] + reqRoster["rb"] + reqRoster["te"]))
    return playersDrafted == rosterTotal
  

# print(minimaxDraft(2, Player.allPlayers, True))



