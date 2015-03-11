# Project 4: Othello Game Logic

class InvalidOthelloMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass

class OthelloGame:
    def __init__(self, row:int, col:int, turn:str, top_left:str, most:bool):
        '''Initializes the OthelloGame class object'''
        self._row = row
        self._col = col
        self._turn = turn
        self._top_left = top_left
        self._most = most
        self._board = self._new_board(row, col, top_left)
        self._winner = None
        self._directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]

    def get_board(self)->[[str]]:
        '''Returns the game board as a list of list of strings'''
        return self._board
    
    def get_turn(self)->str:
        '''Returns which player's turn it is'''
        return self._turn

    def get_winner(self)->str:
        '''Returns the winning player'''
        return self._winner

    def disc_count(self, s:str)->int:
        '''Returns the number of discs of indicated player'''
        result = 0
        for row in self._board:
            for col in row:
                if col == s:
                    result += 1
        return result

    def make_move(self, row:int, col:int)->None:
        '''If move is valid, execute move and update winning state, otherwise raise invalid move exception'''
        if not (self._is_valid_move(row, col)) or self._winner != None:
            raise InvalidOthelloMoveError()
        flip_list = self._flip_list(row, col)
        for x,y in flip_list:
            self._board[x][y] = self._turn
        self._board[row-1][col-1] = self._turn
        self._update_winning_state()

    def _is_valid_number(self, n:int)->bool:
        '''Returns True if the given number is valid, returns False otherwise'''
        return 4 <= n <= 16

    def _is_even_number(self, n:int)->bool:
        '''Returns True if the given number is even, returns False otherwise'''
        return n%2 == 0

    def _require_valid_number(self, n:int)->None:
        '''Raises an InvalidOthelloMoveError is its parameter isn't a valid number'''
        if type(n) != int or not (self._is_valid_number(n) and self._is_even_number(n)):
            raise InvalidOthelloMoveError()

    def _new_board(self, row:int, col:int, top_left:str)->[[str]]:
        '''Creates initial game board with four discs in center, starting with top left player
        as indicated'''
        self._require_valid_number(row)
        self._require_valid_number(col)

        board = []
        for r in range(row):
            board.append([])
            for c in range(col):
                board[-1].append('')

        if top_left == 'W':
            top_right = 'B'
        else:
            top_right = 'W'

        board[row//2-1][col//2-1] = top_left
        board[row//2-1][col//2] = top_right
        board[row//2][col//2-1] = top_right
        board[row//2][col//2] = top_left
            
        return board

    def _opposite_turn(self)->str:
        '''Returns the opposite player'''
        if self._turn == 'B':
            return 'W'
        elif self._turn == 'W':
            return 'B'

    def _is_valid_move(self, row:int, col:int)->bool:
        '''Returns True if move is within boundaries of row / col and it's an empty slot, return False otherwise'''
        return row > 0 and col > 0 and row <= self._row and col <= self._col and self._board[row-1][col-1] == '' and self._flip_list(row, col) != []


    def _is_in_board(self, row:int, col:int)->bool:
        '''Returns True if move is within the board boundaries, returns False otherwise'''
        return row >= 0 and col >= 0 and row < self._row and col < self._col
    
    def _check_valid_moves(self)->bool:
        '''Returns True if the opposite player still has valid moves, returns False otherwise'''
        self._turn = self._opposite_turn()
        for row in range(self._row):
            for col in range(self._col):
                if self._is_valid_move(row+1, col+1):
                    return True
        return False

    def _update_winning_state(self)->None:
        '''Checks if there are still valid moves, else determine if there's a winnner'''
        # Check if opposite player has valid moves left
        if self._check_valid_moves():
            return None
        # Check if current player has valid moves left
        if self._check_valid_moves():
            return None

        black = self.disc_count('B')
        white = self.disc_count('W')
        if black == white:
            self._winner = 'Tie'
            return None
        elif self._most:
            if black > white:
                self._winner = 'Black'
            else:
                self._winner = 'White'
        else:
            if black < white:
                self._winner = 'Black'
            else:
                self._winner = 'White'

    def _flip_list(self, row:int, col:int)->list:
        '''Returns a list of the opposite pieces that will be flipped'''
        result = []
        for x,y in self._directions:
            opposite = []
            r = row-1+x
            c = col-1+y
            while self._is_in_board(r, c):
                if self._board[r][c] == self._opposite_turn():
                    opposite.append((r,c))
                    r += x
                    c += y
                elif self._board[r][c] == self._turn:
                    result.extend(opposite)
                    break
                else:
                    break
        return result