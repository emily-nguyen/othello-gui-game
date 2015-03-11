# Project 5: Othello GUI w/ Tkinter

import tkinter
import othello_game_logic 

class OthelloGUI:
    def __init__(self):
        '''Initializes the OthelloGUI class object'''
        self._root_window = tkinter.Tk()

class DialogWindow:
    def __init__(self):
        '''Initializes the DialogWindow class object'''
        self._dialog_window = tkinter.Toplevel() 

        # Row label
        self._row_label = tkinter.Label(master=self._dialog_window, text='Rows ')
        self._row_label.grid(row=0, column=0, sticky=tkinter.W)
        # Row drop down menu
        self._row = tkinter.IntVar()
        self._row.set(4)
        self._row = tkinter.OptionMenu(self._dialog_window, self._row, 4, 6, 8, 10, 12, 14, 16)
        self._row.grid(row=0, column=1, sticky=tkinter.W)

        # Column label
        self._col_label = tkinter.Label(master=self._dialog_window, text='Columns ')
        self._col_label.grid(row=1, column=0, sticky=tkinter.W)
        # Column drop down menu
        self._col = tkinter.IntVar()
        self._col.set(4)
        self._row = tkinter.OptionMenu(self._dialog_window, self._col, 4, 6, 8, 10, 12, 14, 16)
        self._col.grid(row=1, column=1, sticky=tkinter.W)

        # Turn label
        self._turn_label = tkinter.Label(master=self._dialog_window, text='Starting Player ')
        self._turn_label.grid(row=2, column=0, sticky=tkinter.W)
        # Turn drop down menu
        self._turn = tkinter.StringVar()
        self._turn.set('Black')
        self._turn = tkinter.OptionMenu(self._dialog_window, self._turn, 'Black', 'White')
        self._turn.grid(row=2, column=1, sticky=tkinter.W)

        # Top left label
        self._top_left_label = tkinter.Label(master=self._dialog_window, text='Top Left Disc ')
        self._top_left_label.grid(row=3, column=0, sticky=tkinter.W)
        # Top left drop down menu
        self._top_left = tkinter.StringVar()
        self._top_left.set('Black')
        self._top_left = tkinter.OptionMenu(self._dialog_window, self._top_left, 'Black', 'White')
        self._top_left.grid(row=3, column=1, sticky=tkinter.W)

        # Most discs win label
        self._most_label = tkinter.Label(master=self._dialog_window, text='Most Discs Win? ')
        self._most_label.grid(row=4, column=0, sticky=tkinter.W)
        # Most discs drop down menu
        self._most = tkinter.StringVar()
        self._most.set('Yes')
        self._most = tkinter.OptionMenu(self._dialog_window, self._most, 'Yes', 'No')
        self._most.grid(row=4, column=1, sticky=tkinter.W)