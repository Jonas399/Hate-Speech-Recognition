"""
gui.py to use via GUI

"""
import tkinter as tk


class GUI:

    def __init__(self, window):

        self.window = window

        # init constants
        w_width = 1000
        w_height = 600

        # set title
        self.window.title('Hate Speech Detection Bot')

        # get screen geometry
        s_width = self.window.winfo_screenwidth() # width of screen
        s_height = self.window.winfo_screenheight() # height of screen

        w_x = (s_width/2) - (w_width/2)
        w_y = (s_height/2) - (w_height/2)

        # set window geometry and pos @start
        self.window.geometry('%dx%d+%d+%d' % (w_width, w_height, w_x, w_y))


    def handle_click(self):
        pass



if __name__ == '__main__':

    root = tk.Tk()
    GUI(root)
    root.mainloop()





    
    

    






