import tetris1
import numpy as np


figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

#B
def column_height(field):
    h = []
    for j in range(10):

        column = [field[i][j] for i in range(20)]
        hh = 0
        while hh < 20 and column[hh] == 0:

            hh += 1

        h.append(20 - hh)
    return h


def maximum_height(field):
    return(max(column_height(field)))


def column_difference(field):
    c=[]
    h=column_height(field)

    for j in range(9):
        c.append(abs(h[j+1]-h[j]))
    return(c)

def holes(field):
    L = 0
    h  =column_height(field)

    for j in range(10):
        for i in range(20-h[j],20):
            if field[i][j] == 0:
                L+=1
    return(L)

#D

def row_transitions(field):
    transitions = 0
    
    for row in field:
        for col in range(len(row) - 1):
            # Check if there is a transition between current cell and next cell
            if row[col] != row[col + 1]:
                transitions += 1
    
    return transitions

def column_transitions(field):

    transitions = 0
    
    for col in range(len(field[0])):  # Iterate through each column
        for row in range(len(field) - 1):  # Iterate through each row
            # Check if there is a transition between current cell and cell below
            if field[row][col] != field[row + 1][col]:
                transitions += 1
    
    return transitions

def board_wells(field):

    penalty = 0
    
    for col in range(len(field[0])):  # Iterate through each column
        depth = 0
        for i in range(len(field)):  # Iterate through each row
            row = len(field) -1 -i
            if field[row][col] == 0:  # Empty cell
                # Check if the cell is part of a well (empty with filled cells on both sides)
                left_filled = col > 0 and field[row][col - 1] != 0
                right_filled = col < len(field[0]) - 1 and field[row][col + 1] != 0
                
                if left_filled and right_filled:
                    depth += 1  # Increase well depth
                else:
                    if depth > 0:
                        # Add the penalty for the well
                        penalty += depth   
                        depth = 0  # Reset depth for the next well
            else:
                if depth > 0:
                    # Add the penalty for the well
                    penalty += depth
                    depth = 0  # Reset depth for the next well
        
        # Handle wells that extend to the bottom of the field
        if depth > 0:
            penalty += depth
    
    return penalty
#U
def hole_depth(field):

    total_depth = 0
    
    for col in range(len(field[0])):  # Iterate through each column
        for row in range(len(field)):  # Iterate through each row
            if field[row][col] == 0:  # Hole detected
                # Count the number of full cells above the hole
                depth = 0
                for above_row in range(row):
                    if field[above_row][col] != 0:
                        depth += 1
                total_depth += depth
    
    return total_depth


def rows_with_holes(field):

    rows_with_holes_count = 0
    
    for row in range(len(field)):  # Iterate through each row
        has_hole = False
        for col in range(len(field[0])):  # Iterate through each column
            if field[row][col] == 0:  # Hole detected
                has_hole = True
                break  # No need to check further in this row
        if has_hole:
            rows_with_holes_count += 1
    
    return rows_with_holes_count
#UU
def rows_with_two_holes(field):

    rows_with_two_holes_count = 0
    
    for row in range(len(field)):  # Iterate through each row
        hole_count = 0
        for col in range(len(field[0])):  # Iterate through each column
            if field[row][col] == 0:  # Hole detected
                hole_count += 1
                if hole_count >= 2:
                    rows_with_two_holes_count += 1
                    break  # No need to check further in this row
    
    return rows_with_two_holes_count


def square_surrounded_holes(field):

    surrounded_holes_count = 0
    
    for row in range(1, len(field) - 1):  # Avoid boundary rows
        for col in range(1, len(field[0]) - 1):  # Avoid boundary columns
            if field[row][col] == 0:  # Hole detected
                # Check if the hole is surrounded by full cells
                if (
                    field[row - 1][col] != 0  # Top
                    and field[row + 1][col] != 0  # Bottom
                    and field[row][col - 1] != 0  # Left
                    and field[row][col + 1] != 0  # Right
                ):
                    surrounded_holes_count += 1
    
    return surrounded_holes_count**2  # Square the count
#####

def evaluate_B(W, field): 
    h=column_height(field)
    dh=column_difference(field)
    L=holes(field)
    H=maximum_height(field)
    S = 0
    for k in range (len(h)):
        S += h[k] * W[k]
    for k in range (len(dh)):
        S += dh[k] * W[10+k]
    S += W[19] * L
    S += W[20] * H
    return(S)
def evaluate_DU(W, field): 
    features = []

    H=maximum_height(field)
    features.append(H)
    delta_r = row_transitions(field)
    features.append(delta_r)
    delta_c = column_transitions(field)
    features.append(delta_c)
    L = holes(field)
    features.append(L)
    b_w = board_wells(field)
    features.append(b_w)
    h_d = hole_depth(field)
    features.append(h_d)
    r_h = rows_with_holes(field)
    features.append(r_h)
    S = 0

    for i in range(len(W)):
        S+= W[i]*features[i]
    return S
def evaluate_DU2(W, field): 
    features = []

    H=maximum_height(field)
    features.append(H)
    delta_r = row_transitions(field)
    features.append(delta_r)
    delta_c = column_transitions(field)
    features.append(delta_c)
    L = holes(field)
    features.append(L)
    b_w = board_wells(field)
    features.append(b_w)
    s_s_h = square_surrounded_holes(field)
    features.append(s_s_h)
    r_h2 = rows_with_two_holes(field)
    features.append(r_h2)
    S = 0
    for i in range(len(W)):
        S+= W[i]*features[i]
    return S



def evaluate_best_move(W,field,type,features):
    L=[]
    score=[]
    n_rot = len(figures[type])

    
    for k in range (n_rot):
        for col in range (-2,10):
            game_copy = tetris1.Tetris(20,10)
            
            game_copy.field = [[cell for cell in row] for row in field]

            game_copy.new_figure(type)
            game_copy.rotate(k)
            game_copy.go_side(col) 
            

            if not game_copy.intersects():
                game_copy.go_space()

                if features ==0:
                    score.append(evaluate_B(W,game_copy.field))
                if features ==1:
                    score.append(evaluate_DU(W,game_copy.field))
                if features ==2:
                    score.append(evaluate_DU2(W,game_copy.field))

                L.append((col,k))
    if len(L)>0:
        best_move = score.index(min(score))
        return(L[best_move])
    else : 
        return((0,0))
    

#used for the normal settings
def simulation(W,features,ite=1):
    avg = 0
    for i in range(ite):
        game = tetris1.Tetris(20, 10)
        while game.state != "gameover":

            type = np.random.randint(0,6)
            game.new_figure(type)

            col, rot = evaluate_best_move(W,game.field,type,features)
            game.rotate(rot)
            game.go_side(col)
            if game.intersects():
                game.state="gameover"
            
            else:
                game.go_space()

        avg += (game.score)/ite
    return avg

#used for System 2 and 3
def simulation2(W,features,ite = 1):
    avg = 0
    for i in range(ite):
        game = tetris1.Tetris(20, 10)
        while game.state != "gameover":

            type = np.random.randint(0,6)
            game.new_figure(type)

            col, rot = evaluate_best_move(W,game.field,type,features)
            game.rotate(rot)
            game.go_side(col)
            if game.intersects():
                game.state="gameover"
            
            else:
                game.go_space()

        avg += game.ite/ite
    return avg