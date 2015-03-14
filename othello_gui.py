# Project 5: Othello GUI w/ Tkinter

import tkinter
import othello_game_logic 

class OthelloGUI:
    def __init__(self):
        '''Initializes the OthelloGUI class object'''
        self._root_window = tkinter.Tk()
        self._root_window.title('Othello')

        # Create DialogWindow object and display window
        self._input_window = DialogWindow()
        self._input_window.display()
    
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
            self._canvas = tkinter.Canvas(master=self._root_window, width=self._col*50, height=self._row*50, background='green')
            self._canvas.grid(row=0, column=0, padx=20, pady=20, columnspan=2,
                              sticky=tkinter.N + tkinter.S + tkinter.W + tkinter.E)
            self._root_window.rowconfigure(0, weight=1)
            self._root_window.columnconfigure(0, weight=1)
            
            # Get width and height of canvas
            self._width = self._canvas.winfo_width()
            self._height = self._canvas.winfo_height()
            
            # Turn label
            self._t = tkinter.StringVar()
            self._t.set("Player B's turn")
            self._t_label = tkinter.Label(master=self._root_window, textvariable=self._t)
            self._t_label.grid(row=1, column=0, pady=5)
            self._root_window.rowconfigure(1, weight=1)
            self._root_window.columnconfigure(0, weight=1)

            # Most label
            self._m = tkinter.StringVar()
            self._m.set('Most: {}'.format(self._most))
            self._m_label = tkinter.Label(master=self._root_window, textvariable=self._m)
            self._m_label.grid(row=1, column=1, pady=5)
            self._root_window.rowconfigure(1, weight=1)
            self._root_window.columnconfigure(1, weight=1)
            
            # Black score label
            self._b = tkinter.StringVar()
            self._b.set('Black: 2')
            self._b_label = tkinter.Label(master=self._root_window, textvariable=self._b)
            self._b_label.grid(row=2, column=0, pady=5)
            self._root_window.rowconfigure(2, weight=1)
            self._root_window.columnconfigure(0, weight=1)
            
            # White score label
            self._w = tkinter.StringVar()
            self._w.set('White: 2')
            self._w_label = tkinter.Label(self._root_window, textvariable=self._w)
            self._w_label.grid(row=2, column=1, pady=5)
            self._root_window.rowconfigure(2, weight=1)
            self._root_window.columnconfigure(1, weight=1)
            
            # Bind commands
            self._canvas.bind('<Motion>', self._mouse_moved)
            self._canvas.bind('<ButtonRelease-1>', self._make_move)
            self._canvas.bind('<Configure>', self._canvas_resized)

            
    def start(self)->None:
        '''If there are no inputs, destroys the window, otherwise runs the mainloop'''
        if self._othello_game != None:
            self._root_window.mainloop()
        else:
            self._root_window.destroy()

    def _mouse_moved(self, event:tkinter.Event)->None:
        '''Checks if the move that user hovers over is valid and highlights the cell, else if move is invalid, doesn't highlight the cell'''
        self._draw_board()
        
        self._width = self._canvas.winfo_width()
        self._height = self._canvas.winfo_height()
        row = int(event.y/self._height * self._row)
        col = int(event.x/self._width * self._col)
        
        # Creates highlighted cell if move is valid
        if self._othello_game._is_valid_move(row+1, col+1):
            self._canvas.create_rectangle(col/self._col * self._width, row/self._row * self._height, (col+1)/self._col * self._width, (row+1)/self._row * self._height, fill='#00CC66')

    def _update_labels(self)->None:
        '''Gets the number of black / white discs and updates score labels'''
        black = self._othello_game.disc_count('B')
        white = self._othello_game.disc_count('W')
        self._b.set('Black: {}'.format(black))
        self._w.set('White: {}'.format(white))

    def _check_winning_state(self)->None:
        '''Sets the winning state to next turn, tie, or game over'''
        if self._othello_game.get_winner() == None:
            self._t.set("Player {}'s turn".format(self._othello_game.get_turn()))
        elif self._othello_game.get_winner() == 'Tie':
            self._t.set("It's a tie.")
        else:
            self._t.set('{} is the winner!'.format(self._othello_game.get_winner()))
    
    def _draw_board(self)->None:
        '''Draws the current GUI board'''
        self._update_labels()
        self._check_winning_state()
                        
        # Clears the canvas
        self._canvas.delete(tkinter.ALL)
        
        self._width = self._canvas.winfo_width()
        self._height = self._canvas.winfo_height()
                        
        # Draw the lines on the board to create cells
        for row in range(1, self._row):
            row /= self._row
            self._canvas.create_line(0, row*self._height, self._width, row*self._height, fill='black')
        for col in range(1, self._col):
            col /= self._col
            self._canvas.create_line(col*self._width, 0, col*self._width, self._height, fill='black')
        
        # Iterates through the game board and draws the discs
        for row in range(self._row):
            for col in range(self._col):
                board = self._othello_game.get_board()
                if board[row][col] != '':
                    if board[row][col] == 'B':
                        color = 'black'
                    else:
                        color = 'white'
                    self._canvas.create_oval(col/self._col * self._width, row/self._row * self._height, (col+1)/self._col * self._width, (row+1)/self._row * self._height, fill=color)
    
    def _make_move(self, event:tkinter.Event)->None:
        '''Attempts to make a move; if valid, board will be updated with move indicated, else nothing will happen'''
        self._width = self._canvas.winfo_width()
        self._height = self._canvas.winfo_height()
        row = int(event.y/self._height * self._row)
        col = int(event.x/self._width * self._col)
        
        # Tries to make a move and draw board; if invalid move, catch error and do nothing
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
        self._dialog_window.rowconfigure(0, weight=1)
        self._dialog_window.columnconfigure(0, weight=1)
        
        # Row drop down menu
        self._r = tkinter.IntVar()
        self._r.set(4)                # Set default row = 4
        self._row = tkinter.OptionMenu(self._dialog_window, self._r, 4, 6, 8, 10, 12, 14, 16)
        self._row.grid(row=0, column=1, sticky=tkinter.W)
        self._dialog_window.rowconfigure(0, weight=1)
        self._dialog_window.columnconfigure(1, weight=1)

        # Column label
        self._col_label = tkinter.Label(master=self._dialog_window, text='Columns ')
        self._col_label.grid(row=1, column=0, sticky=tkinter.W)
        self._dialog_window.rowconfigure(1, weight=1)
        self._dialog_window.columnconfigure(0, weight=1)
        
        # Column drop down menu
        self._c = tkinter.IntVar()
        self._c.set(4)                # Set default col = 4
        self._col = tkinter.OptionMenu(self._dialog_window, self._c, 4, 6, 8, 10, 12, 14, 16)
        self._col.grid(row=1, column=1, sticky=tkinter.W)
        self._dialog_window.rowconfigure(1, weight=1)
        self._dialog_window.columnconfigure(1, weight=1)

        # Turn label
        self._turn_label = tkinter.Label(master=self._dialog_window, text='Starting Player ')
        self._turn_label.grid(row=2, column=0, sticky=tkinter.W)
        self._dialog_window.rowconfigure(2, weight=1)
        self._dialog_window.columnconfigure(0, weight=1)
        
        # Turn drop down menu
        self._t = tkinter.StringVar()
        self._t.set('Black')         # Set default starting player = Black
        self._turn = tkinter.OptionMenu(self._dialog_window, self._t, 'Black', 'White')
        self._turn.grid(row=2, column=1, sticky=tkinter.W)
        self._dialog_window.rowconfigure(2, weight=1)
        self._dialog_window.columnconfigure(1, weight=1)

        # Top left label
        self._top_left_label = tkinter.Label(master=self._dialog_window, text='Top Left Disc ')
        self._top_left_label.grid(row=3, column=0, sticky=tkinter.W)
        self._dialog_window.rowconfigure(3, weight=1)
        self._dialog_window.columnconfigure(0, weight=1)
        
        # Top left drop down menu
        self._t_l = tkinter.StringVar()
        self._t_l.set('Black')     # Set default top left disc = Black
        self._top_left = tkinter.OptionMenu(self._dialog_window, self._t_l, 'Black', 'White')
        self._top_left.grid(row=3, column=1, sticky=tkinter.W)
        self._dialog_window.rowconfigure(3, weight=1)
        self._dialog_window.columnconfigure(1, weight=1)

        # Most discs win label
        self._most_label = tkinter.Label(master=self._dialog_window, text='Most Discs Win? ')
        self._most_label.grid(row=4, column=0, sticky=tkinter.W)
        self._dialog_window.rowconfigure(4, weight=1)
        self._dialog_window.columnconfigure(0, weight=1)
        
        # Most discs drop down menu
        self._m = tkinter.StringVar()
        self._m.set('Yes')           # Set default most discs win = Yes
        self._most = tkinter.OptionMenu(self._dialog_window, self._m, 'Yes', 'No')
        self._most.grid(row=4, column=1, sticky=tkinter.W)
        self._dialog_window.rowconfigure(4, weight=1)
        self._dialog_window.columnconfigure(1, weight=1)

        # Enter button
        self._enter = False             # Enter button hasn't been clicked yet
        self._enter_button = tkinter.Button(master=self._dialog_window, text='ENTER', command=self._clicked_enter)
        self._enter_button.grid(row=5, column=0, sticky=tkinter.W)
        self._dialog_window.rowconfigure(5, weight=1)
        self._dialog_window.columnconfigure(0, weight=1)
        
        # Cancel button 
        self._cancel_button = tkinter.Button(master=self._dialog_window, text='CANCEL', command=self._clicked_cancel)
        self._cancel_button.grid(row=5, column=1, sticky=tkinter.W)
        self._dialog_window.rowconfigure(5, weight=1)
        self._dialog_window.columnconfigure(1, weight=1)
    
    def display(self)->None:
        '''Displays the dialog window by making the root window wait until dialog window is close'''
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
        '''When enter button is clicked, destroy the dialog window and set enter=True'''
        self._enter = True
        self._dialog_window.destroy()
        
    def _clicked_cancel(self)->None:
        '''When cancel button is clicked, destroy the dialog window'''
        self._dialog_window.destroy()

if __name__ == '__main__':
    OthelloGUI().start()
