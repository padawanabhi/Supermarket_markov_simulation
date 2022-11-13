import cv2
import numpy as np
from PIL import Image

TILE_SIZE = 32

def extract_tile(tiles, location_tuple):
        """extract a tile array from the tiles image"""
        y = location_tuple[0]*TILE_SIZE
        x = location_tuple[1]*TILE_SIZE
        return tiles[y:y+TILE_SIZE, x:x+TILE_SIZE].copy()


def save_tile(name, tile, index):
    cv2.imwrite(f'./images/{name+str(index+1)}.png', tile)


def extract_save_combined(coord_list, name):
    for index, coord in enumerate(coord_list):
        tile = extract_tile(tiles, coord)
        save_tile(name, tile, index)


if __name__ == "__main__":
    tiles = cv2.imread("./images/tiles.png")

    background_loc = [(0,0)]
    door_loc = [(7,3)]
    floor_loc = (0,2)
    customer_loc = [(3,0), (3,1), (3,2), (4,0), (4,1), (4,2), (7,0), (7,1), (7,2)]
    fruits_loc = [(0,4), (1,4), (2,4), (3,4), (4,4)]
    veggie_loc = [(0,11), (1,11), (2,11), (3,11), (4,11)]
    drink_loc = [(3,13), (0,10)]
    dairy_loc = [(0,-2), (1,-2)]
    spice_loc = [(0,3), (1,3), (2,3)]
    counter_loc = [(0,1)]

    extract_save_combined(background_loc, 'background')
    extract_save_combined(door_loc, 'door')
    extract_save_combined(customer_loc, 'customer')
    extract_save_combined(fruits_loc, 'fruit')
    extract_save_combined(veggie_loc, 'vegetable')
    extract_save_combined(drink_loc, 'drink')
    extract_save_combined(dairy_loc, 'dairy')
    extract_save_combined(spice_loc, 'spice')
    extract_save_combined(counter_loc, 'counter')
    floor = extract_tile(tiles, floor_loc)
    floor = floor + 255
    save_tile('floor', floor, 0)