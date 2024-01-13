from board import Ship, Board  # important for the project

## Uncomment the following lines when you are ready to do input/output tests!
## Make sure to uncomment when submitting to Codio.
import sys


def input(prompt=None):
    if prompt != None:
        print(prompt, end="")
    aaa_str = sys.stdin.readline()
    aaa_str = aaa_str.rstrip("\n")
    print(aaa_str)
    return aaa_str


class Player(object):
    """
        Represents a single player of battleship. Responsible for storing and updating
        each player's data: Placing ships during part 1 and reading guesses each turn
        during part 2.
    """

    def __init__(self, name, board, ship_list):
        """
            name: Name of given player (str)
            board: Given board object belonging to player (Board)
            guesses: List of current player's guesses (list of tuples)
            ship_list: list representing the types of ships for the game (list of ints)
        """
        self.name = name
        self.board = board
        self.guesses = []
        self.ship_list = ship_list

    def validate_guess(self, guess):
        """
            Check if given guess is valid.
            guess: given guess (tuple)
        """
        # Validate guess
        if guess not in self.guesses:
            # Check if guess exists on board
            # Not sure if should check for valid location first!
            if int(guess[0]) in range(self.board.size + 1) and int(guess[-1]) in range(self.board.size + 1):
                pass
            else:
                raise RuntimeError("Guess is not a valid location!")
        else:
            raise RuntimeError("This guess has already been made!")

    def get_player_guess(self):
        """
            Read player guess.
            Return: valid guess as tuple
        """
        guess = input("Enter your guess: ")
        try:
            guess = guess.split(",")
            guess = tuple(guess)
            self.validate_guess(guess)
            return guess
        except:
            guess = input("Enter your guess: ")

    def set_all_ships(self):
        """
            Place all ships for the player.
        """
        # Place every ship based on user input
        for ship in self.ship_list:
            unvalid_ship = True
            while unvalid_ship:
                cords = input(f"Enter the coordinates of the ship of size {ship}: ")
                cords = tuple(cords.split(","))
                orientation = input(f"Enter the orientation of the ship of size {ship}: ")
                current_ship = Ship(ship, cords, orientation)

                try:
                    self.board.validate_ship_coordinates(current_ship)
                    self.board.place_ship(current_ship)
                    unvalid_ship = False
                    continue
                except RuntimeError:
                    pass


class BattleshipGame(object):
    """
        Responsible for running the game, keeping track of turns, and checking if a player has won.
    """
    def __init__(self, player1, player2):
        """
            player1: (Player)
            player: (Player)
        """
        self.player1 = player1
        self.player2 = player2

    def check_game_over(self):
        """
            Check if game has ended (all ships belonging to either player have sunk)
            Return: Name of winning player (str)
        """
        # Check if either player has won
        # Count total length of ship lists
        total_ship_length22 = 0
        for ship_length in self.player2.ship_list:
            total_ship_length22 += ship_length

        total_ship_length11 = 0
        for ship_length in self.player1.ship_list:
            total_ship_length11 += ship_length

        # Count "H" in board
        player1_hit_count = 0
        player2_hit_count = 0
        for row in self.player1.board.board:
            for slot in row:
                if slot == "H":
                    player1_hit_count += 1
        for row in self.player2.board.board:
            for slot in row:
                if slot == "H":
                    player2_hit_count += 1

        if total_ship_length22 == player1_hit_count:
            return "Player 1"
        elif total_ship_length11 == player2_hit_count:
            return "Player 2"
        else:
            return ""

    def display(self):
        """
            Displays current state of the game.
        """
        player1_board = self.player1.board
        player2_board = self.player2.board

        print("Player 1's board:")
        print(player1_board)

        print("Player 2's board:")
        print(player2_board)

    def play(self):
        """
            Run entire game until a player has won.
        """
        # Part 1: Each player places their ships
        self.player1.set_all_ships()
        self.player2.set_all_ships()

        # Part 2: Players try to sink eachother's ships until
        # all of one's players ships are sunk
        keep_playing = "c"
        while keep_playing != "q":
            self.display()  # Display boards before turn

            # Apply player 1's guess to player 2's board
            print("Player 1's turn.")
            player1_guess = self.player1.get_player_guess()

            self.player2.board.apply_guess(player1_guess)
            game_ova = self.check_game_over()
            if game_ova != "":
                print("Player 1 wins!")
                exit()

            # Vice versa
            print("Player 2's turn.")
            player2_guess = self.player2.get_player_guess()
            self.player1.board.apply_guess(player2_guess)
            game_ova = self.check_game_over()
            if game_ova != "":
                print("Player 2 wins!")
                exit()

            # Ask if users want to continue playing
            keep_playing = input("Continue playing?: ")
