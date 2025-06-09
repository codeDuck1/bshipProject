# Project 08
# Program the game of Battleship using classes.

# Includes Ship, Board, Player, and Battleship classes to
# implement game mechanics and rules.

from board import Ship, Board  # important for the project
from game import Player, BattleshipGame  # important for the project


def main():
    board_size = 5
    ship_list = [5, 4, 3, 3, 2]

    # Initialize both player's board ob, player ob, and start the game!
    player1_board = Board(board_size)
    player2_board = Board(board_size)

    player1 = Player("Player 1", player1_board, ship_list)
    player2 = Player("Player 2", player2_board, ship_list)

    bship_game = BattleshipGame(player1, player2)
    bship_game.play()


if __name__ == "__main__":
    main()
