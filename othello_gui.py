# Project 5: Othello GUI w/ Tkinter

import tkinter
import othello_game_logic 

class OthelloGUI:
    def __init__(self):
        '''Initializes the OthelloGUI class object'''
        self._root_window = tkinter.Tk()

        # Create DialogWindow object
        self._input_window = DialogWindow()
        self._input_window.show()
    
        # Set instance variable for checking if Othello game has started
        self._othello_game = None
    
        # Check if input window has been closed
        if self._input_window.is_clicked():
            # Set up inital Othello game with inputs
            self._row = self._input_window.row()
            self._col = self._input_window.col()
            self._turn = self._input_window.turn()
            self._top_left = self._input_window.top_left()
            self._most = self._input_window.most()
            self._othello_game = othello_game_logic.OthelloGame(self._row, self._col, self._turn, self._top_left, self._most)
            
            # Create the empty canvas
            self._canvas = tkinter.Canvas(master=self._root_window, width=self._row*50, height=self._col*50, background='green')
            self._canvas.grid(row=0, column=0, padx=20, pady=20, columnspan=3,
                              sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W)
            self._width = self._canvas.winfo_width()
            self._height = self._canvas.winfo_height()
            
            # Bind commands
            self._canvas.bind('<Motion>', self._mouse_moved)
            self._canvas.bind('<ButtonRelease-1>', self._make_move)
            self._canvas.bind('<Configure>', self._canvas_resized)
            
            # Turn label
            self._t = tkinter.StringVar()
            self._t.set("Player B's turn")
            self._t_label = tkinter.Label(master=self._root_window, textvariable=self._t)
            self._t_label.grid(row=1, column=1, pady=10)
            
            # Black score label
            self._b = tkinter.StringVar()
            self._b.set('Black: 0')
            self._b_label = tkinter.Label(master=self._root_window, textvariable=self._b)
            self._b_label.grid(row=1, column=0, pady=10)
            
            # White score label
            self._w = tkinter.StringVar()
            self._w.set('White: 0')
            self._w_label = tkinter.Label(self._root_window, textvariable=self._w)
            self._w_label.grid(row=1, column=2, pady=10)
            
    def start(self)->None:
        '''If there are no inputs, destroys the window, otherwise runs the mainloop'''
        if self._othello_game != None:
            self._root_window.mainloop()
        else:
            self._root_window.destroy()

    def _mouse_moved(self, event:tkinter.Event)->None:
        '''Checks if the move that user hovers over is valid and highlights the cell, else if move is invalid, doesn't highlight the cell'''
        self._width = self._canvas.winfo_width()
        self._height = self._canvas.winfo_height()
 #       row = int(event.x/self._width * self._row)
#        col = int(event.y/self._height * self._col)
        row = int(event.y/self._height * self._row)
        col = int(event.x/self._width * self._col)
        self._draw_board()
        if self._othello_game._is_valid_move(row+1, col+1):
 #           self._canvas.create_rectangle(row/self._row * self._width, col/self._col * self._height, (row+1)/self._row * self._width, (col+1)/self._col * self._height, fill='#00CC66')
            self._canvas.create_rectangle(col/self._col * self._width, row/self._row * self._height, (col+1)/self._col * self._width, (row+1)/self._row * self._height, fill='#00CC66')

    def _check_winning_state(self)->None:
        '''Updates label variables on game board based on winning state'''
        black = self._othello_game.disc_count('B')
        white = self._othello_game.disc_count('W')
        self._b.set('Black: {}'.format(black))
        self._w.set('White: {}'.format(white))
        
        if self._othello_game.get_winner() == None:
            self._t.set("Player {}'s turn".format(self._othello_game.get_turn()))
        elif self._othello_game.get_winner() == 'Tie':
            self._t.set("It's a tie.")
        else:
            self._t.set('{} is the winner!'.format(self._othello_game.get_winner()))
    
    def _draw_board(self)->None:
        '''Draws the current GUI board'''
        self._check_winning_state()
                        
        # Draws the canvas
        self._canvas.delete(tkinter.ALL)
        self._width = self._canvas.winfo_width()
        self._height = self._canvas.winfo_height()
                        
        # Draw the lines on the board to create cells
        for row in range(1, self._row):
            row /= self._row
            self._canvas.create_line(0, row*self._height, self._width, row*self._height, fill='black')
            #self._canvas.create_line(row*self._width, 0, row*self._width, self._height, fill='black')
        for col in range(1, self._col):
            col /= self._col
  #          self._canvas.create_line(0, col*self._height, self._width, col*self._height, fill='black')
            self._canvas.create_line(col*self._width, 0, col*self._width, self._height, fill='black')
        
        # Iterates through game board and draws the discs
        for row in range(self._row):
            for col in range(self._col):
                board = self._othello_game.get_board()
                if board[row][col] != '':
                    if board[row][col] == 'B':
                        color = 'black'
                    else:
                        color = 'white'
                    self._canvas.create_oval(col/self._col * self._width, row/self._row * self._height, (col+1)/self._col * self._width, (row+1)/self._row * self._height, fill=color)
                    #self._canvas.create_oval(row/self._row * self._width, col/self._col * self._height, (row+1)/self._row * self._width, (col+1)/self._col * self._height, fill=color)

    
    def _make_move(self, event:tkinter.Event)->None:
        '''Attempts to make a move; if valid, board will be updated with move indicated, else nothing will happen'''
        self._width = self._canvas.winfo_width()
        self._height = self._canvas.winfo_height()
 #       row = int(event.x/self._width * self._row)
#        col = int(event.y/self._height * self._col)
        row = int(event.y/self._height * self._row)
        col = int(event.x/self._width * self._col)
        print(row, col)
        try:
            self._othello_game.make_move(row+1, col+1)
            self._draw_board()
        except:
            pass
    
    def _canvas_resized(self, event:tkinter.Event):
        '''Reprints the board to match updated size'''
        self._draw_board()

class DialogWindow:
    def __init__(self):
        '''Initializes the DialogWindow class object'''
        self._dialog_window = tkinter.Toplevel() 

        # Row label
        self._row_label = tkinter.Label(master=self._dialog_window, text='Rows ')
        self._row_label.grid(row=0, column=0, sticky=tkinter.W)
        # Row drop down menu
        self._r = tkinter.IntVar()
        self._r.set(4)                # Set default row = 4
        self._row = tkinter.OptionMenu(self._dialog_window, self._r, 4, 6, 8, 10, 12, 14, 16)
        self._row.grid(row=0, column=1, sticky=tkinter.W)

        # Column label
        self._col_label = tkinter.Label(master=self._dialog_window, text='Columns ')
        self._col_label.grid(row=1, column=0, sticky=tkinter.W)
        # Column drop down menu
        self._c = tkinter.IntVar()
        self._c.set(4)                # Set default col = 4
        self._col = tkinter.OptionMenu(self._dialog_window, self._c, 4, 6, 8, 10, 12, 14, 16)
        self._col.grid(row=1, column=1, sticky=tkinter.W)

        # Turn label
        self._turn_label = tkinter.Label(master=self._dialog_window, text='Starting Player ')
        self._turn_label.grid(row=2, column=0, sticky=tkinter.W)
        # Turn drop down menu
        self._t = tkinter.StringVar()
        self._t.set('Black')         # Set default starting player = Black
        self._turn = tkinter.OptionMenu(self._dialog_window, self._t, 'Black', 'White')
        self._turn.grid(row=2, column=1, sticky=tkinter.W)

        # Top left label
        self._top_left_label = tkinter.Label(master=self._dialog_window, text='Top Left Disc ')
        self._top_left_label.grid(row=3, column=0, sticky=tkinter.W)
        # Top left drop down menu
        self._t_l = tkinter.StringVar()
        self._t_l.set('Black')     # Set default top left disc = Black
        self._top_left = tkinter.OptionMenu(self._dialog_window, self._t_l, 'Black', 'White')
        self._top_left.grid(row=3, column=1, sticky=tkinter.W)

        # Most discs win label
        self._most_label = tkinter.Label(master=self._dialog_window, text='Most Discs Win? ')
        self._most_label.grid(row=4, column=0, sticky=tkinter.W)
        # Most discs drop down menu
        self._m = tkinter.StringVar()
        self._m.set('Yes')           # Set default most discs win = Yes
        self._most = tkinter.OptionMenu(self._dialog_window, self._m, 'Yes', 'No')
        self._most.grid(row=4, column=1, sticky=tkinter.W)

        # Enter button
        self._enter = False             # Enter button hasn't been clicked yet
        self._enter_button = tkinter.Button(master=self._dialog_window, text='ENTER', command=self._clicked_enter)
        self._enter_button.grid(row=5, column=1, sticky=tkinter.W)
    
    def show(self)->None:
        '''Shows the dialog window by making the root window wait until dialog window is closed'''
        self._dialog_window.wait_window()
    
    def row(self)->int:
        '''Returns the row from the dialog window row drop down menu'''
        return self._r.get()

    def col(self)->int:
        '''Retunrs the col from the dialog window column drop down menu'''
        return self._c.get()

    def turn(self)->str:
        '''Returns the turn from the dialog window starting player drop down menu'''
        if self._t.get() == 'Black':
            return 'B'
        return 'W'

    def top_left(self)->str:
        '''Returns the color from the dialog window top left disc drop down menu'''
        if self._t_l.get() == 'Black':
            return 'B'
        return 'W'

    def most(self)->str:
        '''Returns True if input is yes from the dialog window most will win drop down menu, returns False otherwise'''
        if self._m.get() == 'Yes':
            return True
        return False

    def is_clicked(self)->bool:
        '''Returns True if enter button has been clicked, returns False otherwise'''
        return self._enter

    def _clicked_enter(self)->None:
        '''When enter button is clicked, destroys the dialog window'''
        self._enter = True
        self._dialog_window.destroy()

if __name__ == '__main__':
    OthelloGUI().start()
