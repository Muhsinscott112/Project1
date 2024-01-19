
"""This class will store all settings for our chess game"""

class Settings():
    def __init__(self): #we initialize the game settings
        # screen dimensions.
        self.WIDTH = 600
        self.HEIGHT = 600
        self.BG_COLOR = ("white")
       
        #board dimensions
        self.ROWS = 8 
        self.COLS = 8
        
        #square size
        self.SQSIZE = self.WIDTH // self.ROWS
        
        self.MAX_FPS = 15 #for animations later on
        self.IMAGES = {} #dictionary of images


        

