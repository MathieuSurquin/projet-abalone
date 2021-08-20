
import copy
import random
from optimizeAI import bigbrainmoves, groupdirection




board = [
			['W', 'W', 'W', 'W', 'B', 'X', 'X', 'X', 'X'],
			['W', 'W', 'W', 'W', 'W', 'W', 'X', 'X', 'X'],
			['E', 'E', 'W', 'W', 'W', 'E', 'E', 'X', 'X'],
			['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'X'],
			['E', 'E', 'E', 'E', 'W', 'E', 'E', 'E', 'E'],
			['X', 'E', 'E', 'E', 'W', 'E', 'E', 'E', 'E'],
			['X', 'X', 'E', 'E', 'B', 'B', 'B', 'E', 'E'],
			['X', 'X', 'X', 'B', 'B', 'B', 'B', 'B', 'B'],
			['X', 'X', 'X', 'X', 'B', 'B', 'B', 'B', 'B']
		]




gamestate = [
            ["W", "W", "W", "W", "W", "X", "X", "X", "X"],
            ["W", "W", "W", "W", "W", "W", "X", "X", "X"],
            ["E", "E", "W", "W", "W", "E", "E", "X", "X"],
            ["E", "E", "E", "B", "E", "E", "E", "E", "X"],
            ["E", "E", "E", "B", "E", "E", "E", "E", "E"],
            ["X", "E", "E", "E", "E", "E", "E", "E", "E"],
            ["X", "X", "E", "E", "B", "B", "B", "E", "E"],
            ["X", "X", "X", "B", "B", "B", "B", "B", "B"],
            ["X", "X", "X", "X", "B", "B", "B", "B", "B"]
		]


directions = {
        'NE': (-1,  0),
        'SW': ( 1,  0),
        'NW': (-1, -1),
        'SE': ( 1,  1),
        'E': ( 0,  1),
        'W': ( 0, -1)
    }


opposite = {
        'NE': 'SW',
        'SW': 'NE',
        'NW': 'SE',
        'SE': 'NW',
        'E': 'W',
        'W': 'E'
    }


lastmoves = []
lastboards =[]

def stateXdisplay(board):
    for i in board:
        pass
        #print(i)

def makemove(state, move, player):
    stateX = copy.deepcopy(state)
    if player == 'B':
        adversary = 'W'
    else:
        adversary = 'B'
    marbles = []
    for item in move[1]:
        if type(item) is tuple:
            marbles.append(list(item))
        else:
            direction = item
    dx, dy = directions[direction]
    xmax, ymax = groupdirection(1,dx, dy,marbles)
    xmin, ymin = groupdirection(-1,dx, dy,marbles)
    stateX[xmin][ymin] = "E"
    if stateX[xmax+dx][ymax+dy] == "E":
        stateX[xmax+dx][ymax+dy] = player
        stateXdisplay(stateX)
        return stateX
    stateX[xmax+dx][ymax+dy] = player
    try:
        if stateX[xmax+2*dx][ymax+2*dy] == adversary and -1 not in (xmax+2*dx,ymax+2*dy):
            try:
                if -1 not in (xmax+3*dx,ymax+3*dy) and stateX[xmax+3*dx][ymax+3*dy] != "X":
                    stateX[xmax+3*dx][ymax+3*dy] = adversary
                stateXdisplay(stateX)
                return stateX
            except IndexError:
                stateXdisplay(stateX)
                return stateX
        else:
            try:
                if -1 not in (xmax+2*dx,ymax+2*dy) and stateX[xmax+2*dx][ymax+2*dy] != "X":
                    stateX[xmax+2*dx][ymax+2*dy] = adversary
                stateXdisplay(stateX)
                return stateX
            except IndexError:
                stateXdisplay(stateX)
                return stateX
    except IndexError:
        stateXdisplay(stateX)
        return stateX


def getkillmoves(moveslist):
    result = []
    for move in moveslist:
        if "kill" in move:
            result.append(move)
    return result

#get the score of the match
def get_score(board,player):
    if player == 'B':
        adversary = 'W'
    else:
        adversary = 'B'
    score = {'player': 0, 'adversary': 0}
    playercount = 0
    adversarycount = 0
    for line in board:
        for column in line:
            if column == player:
                playercount += 1
            if column == adversary:
                adversarycount += 1
    score['player'] = 14 - adversarycount
    score['adversary'] = 14 - playercount
    return score



#Makes better moves than a random AI
def bestmove(state, player):
    if player == 'B':
        adversary = 'W'
    else:
        adversary = 'B'
    moves = bigbrainmoves(state, player)
    if len(moves) == 0:
        return "giveup"
    indice = 0
    for move in moves:
        if move in lastmoves and makemove(state, move, player) in lastboards:
            moves.pop(indice)
        indice+=1
    score = get_score(state, player)
#define priority order of the moves
    killmoves = getkillmoves(moves)
    killmoves = random.sample(killmoves, len(killmoves))
    if len(killmoves) == 0 or (score['adversary'] > 3 and score['player'] <= score['adversary']):
        advkillmoves = getkillmoves(bigbrainmoves(state, adversary))
        if len(advkillmoves) == 0:
		#look for better moves
            neutralmoves = []
            for move in moves:
                if len(getkillmoves(bigbrainmoves(makemove(state, move, player),adversary))) == 0:
                    neutralmoves.append(move)
            if len(neutralmoves) == 0:
                return random.choice(moves)
            escapebordermoves = []
            border = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 5), (2, 0), (2, 6), (3, 0), (3, 7), (4, 0), (4, 8), (5, 1), (5, 8), (6, 2), (6, 8), (7, 3), (7, 8), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]
            for move in neutralmoves:
                for marble in move[1]:
                    if type(marble) == tuple:
                        if marble in border and move[0] not in border:
                            escapebordermoves.append(move)
                            break
            if len(escapebordermoves) == 0:
                getcentermoves = []
                center = [(2,2),(2,3),(2,4),(3,2),(3,3),(3,4),(3,5),(4,2),(4,3),(4,4),(4,5),(4,6),(5,2),(5,3),(5,4),(5,5),(6,2),(6,3),(6,4)]
                for move in neutralmoves:
                    if move[0] in center:
                        getcentermoves.append(move) 
                if len(getcentermoves) == 0:
                    return random.choice(neutralmoves)
                getcentermoves = random.sample(getcentermoves,len(getcentermoves))
                for move in getcentermoves:
                    if len(move[1]) == 4:
                        return move
                for move in getcentermoves:
                    if len(move[1]) == 3:
                        return move
                return random.choice(getcentermoves)
            return random.choice(escapebordermoves)
        else:    
		
            for advmove in random.sample(advkillmoves,len(advkillmoves)):
                marbles = []
                for item in advmove[1]:
                    if type(item) is tuple:
                        marbles.append(item)
                    else:
                        direction = item
                dx, dy = directions[direction]
                xmax, ymax = groupdirection(1,dx, dy,marbles)
                target = (xmax+dx,ymax+dy)
                escapemoves = []
                for move in moves:
                    if target in move[1]:
                        escapemoves.append(move)
                if len(escapemoves) == 0:
                    pushmoves = []
                    for move in moves:
                        if makemove(state, move, player)[xmax][ymax] != adversary:
                            if not len(getkillmoves(bigbrainmoves(makemove(state, move, player),adversary))) > len(advkillmoves): 
                                pushmoves.append(move)
                    if len(pushmoves) == 0:
                        continue
                    return random.choice(pushmoves)
                escapemoves = random.sample(escapemoves, len(escapemoves))
                for move in escapemoves:
                    if len(getkillmoves(bigbrainmoves(makemove(state, move, player),adversary))) == 0:
                       return move
                for move in escapemoves:
                    if len(getkillmoves(bigbrainmoves(makemove(state, move, player),adversary))) > len(advkillmoves):
                        continue
                    return move
            neutralmoves = []
            for move in moves:
                if len(getkillmoves(bigbrainmoves(makemove(state, move, player),adversary))) == 0:
                    neutralmoves.append(move)
            if len(neutralmoves) == 0:
                return random.choice(moves)
            return random.choice(neutralmoves)     
    else:    
        if score['player'] == 5 or score['player'] > score['adversary']:
            return random.choice(killmoves)
        advkillmoves = getkillmoves(bigbrainmoves(state, adversary))
        for move in killmoves:
            if len(getkillmoves(bigbrainmoves(makemove(state, move, player),adversary))) == 0:
                return move
            if len(getkillmoves(bigbrainmoves(makemove(state, move, player),adversary))) > len(advkillmoves):
                continue
        return random.choice(killmoves)
    return random.choice(moves)


#prevents infinite loops
def bestmove_unrepeated(state,player):
    move = bestmove(state, player)
    if len(lastmoves) < 4:
        lastmoves.append(move)
        lastboards.append(makemove(state, move, player))
    else:
        lastmoves.pop(0)
        lastmoves.append(move)
        lastboards.pop(0)
        lastboards.append(makemove(state, move, player))
    return move