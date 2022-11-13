import numpy as np
import cv2
import random
from required_constants import *



class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tiles   : a numpy array containing all the tile images
        """
        self.tiles = tiles
        # split the layout string into a two dimensional matrix
        self.contents = [list(row) for row in layout.split("\n")]
        self.ncols = len(self.contents[0])
        self.nrows = len(self.contents)
        self.image = np.zeros(
            (self.nrows*TILE_SIZE, self.ncols*TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()

    def extract_tile(self, location_tuple):
        """extract a tile array from the tiles image"""
        if location_tuple == FLOOR:
            row = location_tuple[0]*TILE_SIZE
            col = location_tuple[1]*TILE_SIZE
            return self.tiles[row:row+TILE_SIZE, col:col+TILE_SIZE].copy() + 255
        if location_tuple == WALL:
            row = location_tuple[0]*TILE_SIZE
            col = location_tuple[1]*TILE_SIZE
            return self.tiles[row:row+TILE_SIZE, col:col+TILE_SIZE].copy() -10
        else:
            row = location_tuple[0]*TILE_SIZE
            col = location_tuple[1]*TILE_SIZE
            return self.tiles[row:row+TILE_SIZE, col:col+TILE_SIZE].copy()

    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.extract_tile(WALL)
        elif char == "G":
            return self.extract_tile(DOOR)
        elif char == "C":
            return self.extract_tile(COUNTER)
        elif char == "D":
            choice = random.choice(DAIRY)
            return self.extract_tile(choice)
        elif char == "M":
            choice = random.choice(DRINK)
            return self.extract_tile(choice)
        elif char == "F":
            choice = random.choice(FRUIT)
            return self.extract_tile(choice)
        elif char == "S":
            choice = random.choice(SPICE)
            return self.extract_tile(choice)
        else:
            return self.extract_tile(FLOOR)

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.contents):
            for col, char in enumerate(line):
                bm = self.get_tile(char)
                y = row*TILE_SIZE
                x = col*TILE_SIZE
                self.image[y:y+TILE_SIZE, x:x+TILE_SIZE] = bm

    def draw(self, frame):
        """
        draws the image into a frame
        """
        frame[0:self.image.shape[0], 0:self.image.shape[1]] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)


if __name__ == "__main__":

    background = np.zeros((584, 904, 3), np.uint8) + 255
    tiles = cv2.imread("./images/tiles.png")

    market = SupermarketMap(MARKET, tiles)

    while True:
        frame = background.copy()
        market.draw(frame)

        # https://www.ascii-code.com/
        key = cv2.waitKey(1)
       
        if key == 113: # 'q' key
            break
    
        cv2.imshow("frame", frame)


    cv2.destroyAllWindows()

    market.write_image("./images/supermarket.png")
