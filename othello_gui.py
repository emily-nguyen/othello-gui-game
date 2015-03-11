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

    def start(self)->None:
        '''If there are no inputs, destroys the window, otherwise runs the mainloop'''
        self._root_window.mainloop()

class DialogWindow:
    def __init__(self):
        '''Initializes the DialogWindow class object'''
        self._dialog_window = tkinter.Toplevel() 

        # Row label
        self._row_label = tkinter.Label(master=self._dialog_window, text='Rows ')
        self._row_label.grid(row=0, column=0, sticky=tkinter.W)
        # Row drop down menu
        self._row = tkinter.IntVar()
        self._row.set(4)                # Set default row = 4
        self._row = tkinter.OptionMenu(self._dialog_window, self._row, 4, 6, 8, 10, 12, 14, 16)
        self._row.grid(row=0, column=1, sticky=tkinter.W)

        # Column label
        self._col_label = tkinter.Label(master=self._dialog_window, text='Columns ')
        self._col_label.grid(row=1, column=0, sticky=tkinter.W)
        # Column drop down menu
        self._col = tkinter.IntVar()
        self._col.set(4)                # Set default col = 4
        self._col = tkinter.OptionMenu(self._dialog_window, self._col, 4, 6, 8, 10, 12, 14, 16)
        self._col.grid(row=1, column=1, sticky=tkinter.W)

        # Turn label
        self._turn_label = tkinter.Label(master=self._dialog_window, text='Starting Player ')
        self._turn_label.grid(row=2, column=0, sticky=tkinter.W)
        # Turn drop down menu
        self._turn = tkinter.StringVar()
        self._turn.set('Black')         # Set default starting player = Black
        self._turn = tkinter.OptionMenu(self._dialog_window, self._turn, 'Black', 'White')
        self._turn.grid(row=2, column=1, sticky=tkinter.W)

        # Top left label
        self._top_left_label = tkinter.Label(master=self._dialog_window, text='Top Left Disc ')
        self._top_left_label.grid(row=3, column=0, sticky=tkinter.W)
        # Top left drop down menu
        self._top_left = tkinter.StringVar()
        self._top_left.set('Black')     # Set default top left disc = Black
        self._top_left = tkinter.OptionMenu(self._dialog_window, self._top_left, 'Black', 'White')
        self._top_left.grid(row=3, column=1, sticky=tkinter.W)

        # Most discs win label
        self._most_label = tkinter.Label(master=self._dialog_window, text='Most Discs Win? ')
        self._most_label.grid(row=4, column=0, sticky=tkinter.W)
        # Most discs drop down menu
        self._most = tkinter.StringVar()
        self._most.set('Yes')           # Set default most discs win = Yes
        self._most = tkinter.OptionMenu(self._dialog_window, self._most, 'Yes', 'No')
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
        return self._row.get()

    def col(self)->int:
        '''Retunrs the col from the dialog window column drop down menu'''
        return self._col.get()

    def turn(self)->str:
        '''Returns the turn from the dialog window starting player drop down menu'''
        if self._turn.get() == 'Black':
            return 'B'
        return 'W'

    def top_left(self)->str:
        '''Returns the color from the dialog window top left disc drop down menu'''
        if self._top_left.get() == 'Black':
            return 'B'
        return 'W'

    def most(self)->str:
        '''Returns True if input is yes from the dialog window most will win drop down menu, returns False otherwise'''
        if self._most.get() == 'Yes':
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
