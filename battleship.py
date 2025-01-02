"""
battleship.py
Alexander 0gu
4/16/2024
Section 16
alexano2@umbc.edu
This program will display the game of battleship
"""




# THE BOARDS AUTOMATICALLY SWITCH
# PLEASE DON'T MINE THE "SUNK" 1, THEY ARE THE NAMES OF THE SHIPS PRINTED AS NUMBERS
import random




def create_board(board, enemy_board=None, size=10, hidden_ships=True):
   if board is None:
       board = [[' ' for space in range(size)] for space in range(size)]
   if enemy_board is None:
       print("   " + " ".join([f"{i:2}" for i in range(size)]))
       for i in range(size):
           print(f"{i:3}" + "|".join([f"{block:2}" for block in board[i]]) + "|")
   else:
       print("   " + " ".join([f"{i:2}" for i in range(size)]) + "      |   " + " ".join([f"{i:2}" for i in range(size)]))
       for i in range(size):
           enemy_row = []
           for j in range(size):
               if enemy_board[i][j] == 'M':
                   enemy_row.append('M')
               elif enemy_board[i][j] == 'HH' or (not hidden_ships and board[i][j] != ' '):
                   enemy_row.append(board[i][j])
               else:
                   enemy_row.append(' ')
           print(f"{i:3}" + "|".join([f"{cell:2}" for cell in board[i]]) + "|" + "     |" + f"{i:3}" + "|".join([f"{cell:2}" for cell in enemy_row]) + "|")


# This function generates and displays the game boards
# also shows the player's ships and hits or misses on the enemy board




def place_ships(board, ship_number, ship_names, ship_names_inv):
   size = len(board)
   ship_placement = 1
   while ship_placement <= ship_number:
       ship_name, ship_abbreviation, ship_length = ship_names[ship_placement]
       ship_placed = False
       while not ship_placed:
           ship_row_col = input(f"Enter x y coordinates to place the {ship_name}: ")
           ship_row, ship_column = ship_row_col.split()
           if not (ship_row.isdigit() and ship_column.isdigit()):
               print("Use numbers for cords please.")
           else:
               ship_row, ship_column = int(ship_row), int(ship_column)
               if not (0 <= ship_row < size and 0 <= ship_column < size):
                   print("Outta bounds")
               else:
                   placement = input("Enter Right or Down (r or d)").lower()
                   if placement not in ['r', 'd']:
                       print("Invalid, Enter r or d")
                   else:
                       if placement == 'r':
                           if ship_column + ship_length > size:
                               print("Ship doesn't fit, try a different coordinate.")
                           else:
                               choice = False
                               for i in range(ship_length):
                                   if board[ship_row][ship_column + i] != ' ':
                                       print("Ship overlaps, try a different coordinate")
                                       choice = True
                               if not choice:
                                   for i in range(ship_length):
                                       board[ship_row][ship_column + i] = ship_abbreviation
                                   ship_placed = True
                       elif placement == 'd':
                           if ship_row + ship_length > size:
                               print("Ship doesn't fit, try a different coordinate.")
                           else:
                               choice = False
                               for i in range(ship_length):
                                   if board[ship_row + i][ship_column] != ' ':
                                       print("Ship overlaps with another ship. Choose another location.")
                                       choice = True
                               if not choice:
                                   for i in range(ship_length):
                                       board[ship_row + i][ship_column] = ship_abbreviation
                                   ship_placed = True
       ship_placement += 1
       create_board(board)


# This function allows players to input coordinates to place their ships on the board
# It also ensures that ships do not overlap and fit within the board boundaries




def check_guess(board, guess_row, guess_col, ship_names_inv):
   hit_ship = None
   if board[guess_row][guess_col] in ship_names_inv:
       hit_ship = board[guess_row][guess_col]
       board[guess_row][guess_col] = 'HH'
       if all(hit_ship == 'HH' for row in board for hit_ship in row if hit_ship == board[guess_row][guess_col]):
           print(f"You sunk the {ship_names_inv[hit_ship]}")
   else:
       print("Missed")
       board[guess_row][guess_col] = 'M'
   if hit_ship:
       return hit_ship


# This function checks if a guess by a player hits or misses a ship on the opponent's board
# It also updates the board accordingly and indicates if a ship is sunk




def play_battleship(size, num_ships, ship_names):
   ship_names_inv = {abbreviation: name for name, (full_name, abbreviation, _) in ship_names.items()}
   print("Player 1, prepare to place your fleet.")
   empty_board = [[' ' for _ in range(size)] for _ in range(size)]
   create_board(empty_board)
   board1 = [[' ' for _ in range(size)] for _ in range(size)]
   place_ships(board1, num_ships, ship_names, ship_names_inv)
   create_board(board1)
   print("Player 2, prepare to place your fleet.")
   board2 = [[' ' for _ in range(size)] for _ in range(size)]
   place_ships(board2, num_ships, ship_names, ship_names_inv)
   create_board(board2)
   boards = [board1, board2]
   players = ['Player 1', 'Player 2']
   current_player = 0
   attempts = 0
   all_attempts = size * size // 2
   while attempts < all_attempts:
       print(f"{players[current_player]}, it's your turn.")
       opponent_board = boards[1 - current_player]
       create_board(boards[current_player], opponent_board, size)
       guess_coordinates = input("Enter x y coordinate to fire: ").split()
       while len(guess_coordinates) != 2:
           print("Invalid input. Enter coordinates")
           guess_coordinates = input("Enter x y coordinate to fire: ").split()
       guess_row, guess_col = map(int, guess_coordinates)
       if guess_row < 0 or guess_row >= size or guess_col < 0 or guess_col >= size:
           print("Out of bounds.")
       elif opponent_board[guess_row][guess_col] == 'HH' or opponent_board[guess_row][guess_col] == 'M':
           print("You've already guessed this coordinate")
       else:
           hit_ship = check_guess(opponent_board, guess_row, guess_col, ship_names_inv)
           if hit_ship:
               print(f"You hit {players[1 - current_player]}'s {ship_names_inv[hit_ship]}")
           create_board(boards[current_player], opponent_board, size)
           if all('Ca' and 'Ba' and 'Cr' and 'Su' and 'De' not in row for row in opponent_board):
               print(f"{players[current_player]} has won.")
               return
           current_player = 1 - current_player
           attempts += 1
   print("Game Over")


# This function creates the gameplay loop while managing the placement of ships for both players
# It also handles turns, and determines the game's outcome




if __name__ == '__main__':
   ship_names = {
       1: ("Carrier", "Ca", 5),
       2: ("Battleship", "Ba", 4),
       3: ("Cruiser", "Cr", 3),
       4: ("Submarine", "Su", 3),
       5: ("Destroyer", "De", 2)
   }
   play_battleship(10, 5, ship_names)











