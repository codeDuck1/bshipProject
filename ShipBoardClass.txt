import copy


class Ship(object):
    """
        Represents a piece in the Battleship game.
    """
    def __init__(self, length, position, orientation, hit_count=0, is_sunk=False):
        """
            Creates a Ship piece.
            length: Length of ship (int)
            orientation: Orientation of ship (str)
            position: Position on board occupied by ship (list of tuples)
            hit_count: # of hits on ship (int)
            is_sunk: Status of ship (bool)

        """
        self.length = length
        self.orientation = orientation

        # Create list of position tuples based on given position, length and orientation.
        positions = []
        positions.append(position)  # append initial position to list
        for cord in range(length - 1):
            if orientation == "h":
                position = (position[0], int(position[-1]) + 1)
                positions.append(position)
            if orientation == "v":
                position = (int(position[0]) + 1, position[-1])
                positions.append(position)
        self.positions = positions
        self.hit_count = hit_count
        self.is_sunk = is_sunk

    def get_positions(self):
        """
            Returns: list of positions of the Ship
        """
        return self.positions

    def get_orientation(self):
        """
            Returns: the orientation of the Ship.
        """
        return self.orientation

    def apply_hit(self):
        """
            Increases hit count and check if ship is sunk.
        """
        self.hit_count += 1

        # Check if ship is sunk by comparing hit count to
        # length of ship.
        ship_length = len(self.get_positions())
        if self.hit_count >= ship_length:
            self.is_sunk = True


class Board(object):
    """
        Represents board object. Keeps track of ships on board, and assists with validating
        player moves.
    """
    def __init__(self, size):  # dont have to initialize here bc given if?
        """
            size: dimensions of the square board (int)
            board: data structure storing board state (list of lists)
            ships: list of ships on current board
        """
        # if ships is None:
        #     ships = []
        self.size = size

        # Create board with given size dimension.
        board = []
        inner_slots = []
        for x in range(size):
            inner_slots.append(" ")
        for x in range(size):
            board.append(copy.deepcopy(inner_slots))  # MUST BE A DEEP/ MAYBE SHALLOW COPY!!!

        self.board = board
        self.ships = []

    def place_ship(self, ship):
        """
            ship: ship object
        """
        # Update ship list with given ship
        self.ships.append(ship)

        # Retrieve given ship's positions (list of tuples)
        ship_position = ship.get_positions()

        # Find given location tuple within the board list of lists.
        # If row location and slot found, place S within that list at tuples 2nd val (slot).
        for location in ship_position:
            for index, row in enumerate(self.board):
                for index2, slot in enumerate(row):
                    if int(location[0]) == index and int(location[-1]) == index2:
                        row[int(location[-1])] = "S"



                            # longer way: self.board[location[0]][location[-1]] = "S"




    def apply_guess(self, guess):
        """
            guess: Given player guess (tuple)
        """
        # Same logic as prior usage.
        for index, row in enumerate(self.board):
            for index2, slot in enumerate(row):
                if int(guess[0]) == index and int(guess[-1]) == index2:
                    if row[int(guess[-1])] == "S":
                        row[int(guess[-1])] = "H"
                        # Updates ship hit count. Figure out which ship has been hit:
                        # This guess can only belong to one ship.
                        for ship in self.ships:
                            for given_ship_tup in ship.get_positions(): # list of tupes for given ship
                                if (int(guess[0]) == int(given_ship_tup[0]) and int(guess[-1]) ==
                                        int(given_ship_tup[-1])):
                                    ship.apply_hit()
                                    print("Hit!")
                    else:  # missed guess
                        row[int(guess[-1])] = "M"
                        print("Miss!")


    def validate_ship_coordinates(self, ship):
        """
            Checks if given ship object can be placed on current board.
            ship = Given ship (Ship)
        """
        # Retrieve given ship's positions (list of tuples)
        ship_position = ship.get_positions()

        # Ensure ship coords are not already occupied. Same logic
        # as the following.
        occ_count = 0
        for location in ship_position:
            for index, row in enumerate(self.board):
                for index2, slot in enumerate(row):
                    if int(location[0]) == index and int(location[-1]) == index2:
                        if row[int(location[-1])] == "S":  # Check if slot is  occupied
                            occ_count += 1

        if occ_count == len(ship_position):
            print("Ship coordinates are already taken!")
            raise RuntimeError("Ship coordinates are already taken!")

        # Ensure ship coordinates are valid positions on the board.
        # Compare each of ship's tuples to board. If present, add 1
        # to valid_points to track.
        valid_points = 0
        for location in ship_position:
            for index, row in enumerate(self.board):
                for index2, slot in enumerate(row):
                    if int(location[0]) == index and int(location[-1]) == index2:
                        valid_points += 1
        if valid_points != len(ship_position):
            print("Ship coordinates are out of bounds!")
            raise RuntimeError("Ship coordinates are out of bounds!")

    def __str__(self):
        """
            Return: current board as string
        """
        board_string = ""
        for row in self.board:
            board_string += "\n"
            for slot in row:
                board_string += f"[{slot}]"
        board_string = board_string.strip() # remove top blank line
        board_string += "\n"
        return board_string

