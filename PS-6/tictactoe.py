#from functools import lru_cache
from time import time  # time elapsed is now reported

BLANK = ' '
PRINT = 2000000  # this is set somewhat reasonable for 4x4 (could increase if it's producing too much output)

states_examined = 0
seen_set = set()
seen_list = []
terminals_found = 0
start_time = time()

def init_globals():
    global states_examined, seen_set, seen_list, terminals_found, start_time
    states_examined = 0
    seen_set = set()
    seen_list = []
    terminals_found = 0
    start_time = time()
  
def print_globals():
    global states_examined, seen_set, seen_list, terminals_found
    print("states / terminals / unique states / time elapsed (s)", states_examined, terminals_found, len(seen_set), time()-start_time)
    print("\n")
  
def is_terminal(state):
    blanks = state.count(BLANK)
    # BEWARE THE COMMENT AND CODE BELOW IT WHEN CHANGING to 4x4
    # a win requires at least 5 moves = <= 4 blanks in 3X3
    # a win requires at least 7 moves = <= 9 blanks in 4X4
    if blanks>9: return False
    # all states filled
    if blanks==0: return True
    # check for 3 in a row
    if state[0:4]=='XXXX' or state[0:4]=='OOOO': return True
    if state[4:8]=='XXXX' or state[4:8]=='OOOO': return True
    if state[8:12]=='XXXX' or state[8:12]=='OOOO': return True
    if state[12:16]=='XXXX' or state[12:16]=='OOOO': return True
    # check for 3 in a column
    if state[0]+state[4]+state[8]+state[12]=='XXXX' or state[0]+state[4]+state[8]+state[12]=='OOOO': return True
    if state[1]+state[5]+state[9]+state[13]=='XXXX' or state[1]+state[5]+state[9]+state[13]=='OOOO': return True
    if state[2]+state[6]+state[10]+state[14]=='XXXX' or state[2]+state[6]+state[10]+state[14]=='OOOO': return True
    if state[3]+state[7]+state[11]+state[15]=='XXXX' or state[3]+state[7]+state[11]+state[15]=='OOOO': return True
    # check for 3 in a diagonal
    if state[0]+state[5]+state[10]+state[15]=='XXXX' or state[0]+state[5]+state[10]+state[15]=='OOOO': return True
    if state[3]+state[6]+state[9]+state[12]=='XXXX' or state[3]+state[6]+state[9]+state[12]=='OOOO': return True
    return False

def utility(state):
    umap = {True: 1, False: -1}
    # check for 3 in a row
    if state[0:4]=='XXXX' or state[0:4]=='OOOO': return umap[state[0]=='X']
    if state[4:8]=='XXXX' or state[4:8]=='OOOO': return umap[state[4]=='X']
    if state[8:12]=='XXXX' or state[8:12]=='OOOO': return umap[state[8]=='X']
    if state[12:16]=='XXXX' or state[12:16]=='OOOO': return umap[state[12]=='X']
    # check for 3 in a column
    if state[0]+state[4]+state[8]+state[12]=='XXXX' or state[0]+state[4]+state[8]+state[12]=='OOOO': return umap[state[0]=='X']
    if state[1]+state[5]+state[9]+state[13]=='XXXX' or state[1]+state[5]+state[9]+state[13]=='OOOO': return umap[state[1]=='X']
    if state[2]+state[6]+state[10]+state[14]=='XXXX' or state[2]+state[6]+state[10]+state[14]=='OOOO': return umap[state[2]=='X']
    if state[3]+state[7]+state[11]+state[15]=='XXXX' or state[3]+state[7]+state[11]+state[15]=='OOOO': return umap[state[3]=='X']
    # check for 3 in a diagonal
    if state[0]+state[5]+state[10]+state[15]=='XXXX' or state[0]+state[5]+state[10]+state[15]=='OOOO': return umap[state[0]=='X']
    if state[3]+state[6]+state[9]+state[12]=='XXXX' or state[3]+state[6]+state[9]+state[12]=='OOOO': return umap[state[3]=='X']
    return 0

def new_node(state):
    global states_examined, seen_set, seen_list
    states_examined += 1
    seen_set.add(state)
    # COMMENTED OUT TO SAVE MEMORY FOR THE 4x4 CASE
    # seen_list.append(state)
    if states_examined%PRINT==0:
        print("... states examined =", states_examined, ", terminals found =", terminals_found, ", unique stored =", len(seen_set), ", time elapsed (s) =", time()-start_time)
    
def next_state(state, move):
    assert state[move]==BLANK
    # BEWARE THE LINE BELOW WHEN CHANGING TO 4x4
    if state.count(BLANK)%3==1:
        turn = 'X'
    else:
        turn = 'O'
    new_state = state[:move]+turn+state[move+1:]
    return new_state

def get_available_moves(state):
    # player can move to any blank space
    return [i for i in range(len(state)) if state[i]==BLANK]

def minimax_decision(state):
    global terminals_found
    best_moves = []
    if is_terminal(state):
        terminals_found += 1
        return utility(state), best_moves
    moves = get_available_moves(state)
    best_score = float('-inf')
    for move in moves:
        new_state = next_state(state,move)
        new_node(new_state)
        score = min_value(new_state)
        if score > best_score:
            best_moves = [move]
            best_score = score
        elif score == best_score:
            best_moves.append(move)
    return best_score, best_moves

def max_value(state):
    global terminals_found
    if is_terminal(state):
        terminals_found += 1
        return utility(state)
    v = float('-inf')
    moves = get_available_moves(state)
    for move in moves:
        new_state = next_state(state,move)
        new_node(new_state)
        v = max(v, min_value(new_state))
    return v

def min_value(state):
    global terminals_found
    if is_terminal(state):
        terminals_found += 1
        return utility(state)
    v = float('inf')
    moves = get_available_moves(state)
    for move in moves:
        new_state = next_state(state,move)
        new_node(new_state)
        v = min(v, max_value(new_state))
    return v

def print_out(state):
    for r in range(4):
        for c in range(4):
            if c<3:
                endchar = '|'
            else:
                endchar = '\n'
            print(' '+state[r*4+c]+' ',end=endchar)
        if r<3:
            print(('-'*3+'+')*3+'-'*3)

test_boards = ['XXXXOOO'+BLANK*9,
               'OOOOXXX'+BLANK*9,
               'XXX'+BLANK+'OXXOOXXO'+BLANK+'OOO',
               BLANK+'XX'+BLANK+'OXXOOXXO'+BLANK+'OO'+BLANK,
               BLANK*4+'OXXOOXXO'+BLANK*4,
               'XOOO'+BLANK+'X'+BLANK*4+'X'+BLANK*5]

"""
test_boards = ['XXXXOOO'+BLANK*9,
               'OOOOXXX'+BLANK*9,
               'XXX'+BLANK+'OXXOOXXO'+BLANK+'OOO',
               BLANK+'XX'+BLANK+'OXXOOXXO'+BLANK+'OO'+BLANK,
               BLANK*4+'OXXOOXXO'+BLANK*4,
               'XOOO'+BLANK+'X'+BLANK*4+'X'+BLANK*5,
               'X'+BLANK*15,
               BLANK+'X'+BLANK*14,
               BLANK*5+'X'+BLANK*10,
               BLANK*16]
"""

for init in test_boards:
    init_globals()
    print_out(init)
    print("value of game, move =",minimax_decision(init))
    print_globals()
  
print("="*70)
print('\n')

#@lru_cache(maxsize=None)
def alpha_beta_searchRN(state,alpha=float('-inf'),beta=float('inf')):
    global terminals_found
    if is_terminal(state):
        terminals_found += 1
        return utility(state)
    v = max_value(state,alpha,beta)
    return v

def max_value(state,alpha,beta):
    global terminals_found
    if is_terminal(state):
        terminals_found += 1
        return utility(state)
    v = float('-inf')
    # v = alpha # this gives the same nodes expanded as using the line above
    moves = get_available_moves(state)
    for move in moves:
        new_state = next_state(state,move)
        new_node(new_state)
        v = max(v, min_value(new_state,alpha,beta))
        if v >= beta:
            break
        alpha = max(alpha, v)
    return v

def min_value(state,alpha,beta):
    global terminals_found
    if is_terminal(state):
        terminals_found += 1
        return utility(state)
    v = float('inf')
    # v = beta # this gives the same nodes expanded as using the line above
    moves = get_available_moves(state)
    for move in moves:
        new_state = next_state(state,move)
        new_node(new_state)
        v = min(v, max_value(new_state,alpha,beta))
        if v <= alpha:
            break
        beta = min(beta, v)
    return v

for init in test_boards:
    init_globals()
    print_out(init)
    # USING -1 AND 1 FOR ALPHA, BETA BELOW USES A LITTLE MEMORY
    print("value of game =",alpha_beta_searchRN(init,float('-inf'),float('inf')))
    print_globals()