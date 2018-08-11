# DUNGEON ASCII GAME

import os
import random
import time

NO_OF_ROWS_COLS = 5 # The number of rows and columns that will define our square grid
LIST_OF_CELLS = list(range(NO_OF_ROWS_COLS * NO_OF_ROWS_COLS)) # Gets a list of cell indexes from 0 to NO_OF_ROWS_COLS - 1
LENGTH_OF_CELLS = len(LIST_OF_CELLS)

GRID_OF_CELLS = [] # Contains a list of tuples which are the cell positions i.e. (0, 0), (0, 1) etc

# Creates our grid of cells
def create_grid():
    x = 0
    y = 0
    for cell in LIST_OF_CELLS:
        if y != NO_OF_ROWS_COLS: # If we haven't reached the maximum number of rows
            if x != NO_OF_ROWS_COLS: # If we haven't reached the maximum number of columns
                cell_tuple = (x, y) # Cell position i.e (0, 0), (0, 1)
                GRID_OF_CELLS.append(cell_tuple) # Add tuple to our list of cell positions
                x += 1 # Increment x (column) position
            else: # If we have reached the maximum number of columns
                x = 0 # Reset x (column) position to 0
                y += 1 # Increment y (row) position
                cell_tuple = (x, y)
                GRID_OF_CELLS.append(cell_tuple)
                x += 1
        # Moves on to the next cell in the list

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Randomly gets the locations of the player, monster and door. 
# The .sample() function makes sure that the three entities don't get the same value.
def get_locations():
    return random.sample(GRID_OF_CELLS, 3)

# Returns the valid moves that a player can make
def get_moves(character):
    moves = ["LEFT", "RIGHT", "UP", "DOWN"] # List 
    x, y = character # Unpacks the character tuple into x and y co-ordinates
    if x == 0: # Player can't move left if he/she is at the left-most cell.
        moves.remove("LEFT")
    if x == NO_OF_ROWS_COLS - 1: # Player can't move right if he/she is at the right-most cell.
        moves.remove("RIGHT")
    if y == 0: # Player can't move up if he/she is at the top-most cell.
        moves.remove("UP")
    if y == NO_OF_ROWS_COLS - 1: # Player can't move down if he/she is at the bottom-most cell.
        moves.remove("DOWN")
    return moves # Returns a list of moves

# Moves player
def move_player(player, move):
    x, y = player
    if move == "LEFT":
        x -= 1
    if move == "RIGHT":
        x += 1
    if move == "UP":
        y -= 1
    if move == "DOWN":
        y += 1
    return x, y # Returns a tuple with the player's new position

# Moves monster
def move_monster(monster, moves):
    x, y = monster
    monster_move = random.sample(moves, 1) # Get random monster move from the list of valid moves
    monster_move = monster_move[0] # Get string in list item
    if monster_move == "LEFT":
        x -= 1
    if monster_move == "RIGHT":
        x += 1
    if monster_move == "UP":
        y -= 1
    if monster_move == "DOWN":
        y += 1
    return x, y


# Draws the cells of the grid
def draw_map(player, monster):
    print(" _" * NO_OF_ROWS_COLS) # The top wall of the grid
    tile = "|{}"
    
    for cell in GRID_OF_CELLS:
        x, y = cell # Unpack into x and y
        if x < NO_OF_ROWS_COLS - 1: # Not at the end (Right side) of the grid
            line_end = "" # Space at the end of the print statement instead of a new line
            if cell == player: # If cell & player are at same place
                output = tile.format("X")
            elif cell == monster: # If cell & monster are at same place
                output = tile.format("M")
            else:
                output = tile.format("_") # Cell
        else: # At the end (Right side) of the grid
            line_end = "\n"
            if cell == player: # If cell & player are at same place
                output = tile.format("X|")
            elif cell == monster: # If cell & monster are at same place
                output = tile.format("M|")
            else:
                output = tile.format("_|")# Cell with wall to the right
        print(output, end=line_end) # Print the line
            
# The Game Loop
def game_loop():
    # Unpacking?
    monster, door, player = get_locations()
    playing = True
    
    while playing:
        clear_screen()
        draw_map(player, monster)
        valid_player_moves = get_moves(player)
        valid_monster_moves = get_moves(monster)
        
        print("You're currently in room {}".format(player)) # Fill with player position
        print("You can move {}".format(", ".join(valid_player_moves))) # Fill with available moves
        print("")
        print("The monster is currently in room {}".format(monster)) # Fill with monster position
        print("It can move {}".format(", ".join(valid_monster_moves))) # Fill with available moves
        print("")
        print("Enter QUIT to quit")
        
        # User input coverted to upper case to check if move is in list of moves
        move = input(" >")
        move = move.upper()
        
        if move == 'QUIT':
            print("\n ** See you next time ** \n")
            break
        elif move in valid_player_moves:
            player = move_player(player, move) # Player moves
            
            if player == monster:
                print("\n ** Oh no! The monster got you! Better luck next time! ** \n")
                playing = False
            if player == door:
                print("\n ** You escaped! Congratulations! ** \n")
                playing = False
        else:
            print("\n ** Walls are hard! Don't run into them! **\n")
            time.sleep(2)

        # Move monster
        print("The monster is moving...")
        time.sleep(1)
        monster = move_monster(monster, valid_monster_moves) # Pass in monster's position and valid moves

        # Check if monster collides with player
        if monster == player:
            print("\n ** Oh no! The monster got you! Better luck next time! ** \n")
            playing = False
        if monster == door:
            print("\n ** Oh no! The monster has found the door! Now you can't escape! Better luck next time! ** \n")
            playing = False
    else:
        if input("Play again? [Y/N] ").lower() != "n":
            game_loop()
         
# Entry point into game   
clear_screen()
create_grid()
print("Welcome to the dungeon!")
print("Find the invisible door to escape!")
input("Press enter to start!")
clear_screen()
game_loop()
  