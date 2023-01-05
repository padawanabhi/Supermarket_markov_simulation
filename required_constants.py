import numpy as np
from enum import Enum
import pandas as pd
import cv2
from faker import Faker

fake = Faker()

TILE_SIZE = 32

FIRST_SECTION = pd.read_csv('./data/final_data/first_section.csv')

CUSTOMER_PRESENT_FILE = './data/final_data/average_customer_per_min.csv'

CUSTOMER_PER_SECTION = './data/final_data/customers_per_section.csv'

customer_present_df = pd.read_csv(CUSTOMER_PRESENT_FILE, parse_dates=True, index_col='time')


trans = pd.read_csv('./data/final_data/transition_matrix.csv', index_col=0)

supermarket_image = cv2.imread('./images/supermarket.png')


customer_images = []
for i in range(1,10):
    customer_images.append(cv2.imread(f'./images/customer{i}.png'))


MARKET = """
######################
##..................##
#S...SF...FM...MD...D#
#S...SF...FM...MD...D#
#S...SF...FM...MD...D#
#S...SF...FM...MD...D#
#S...SF...FM...MD...D#
#....................#
#....CC...CC...CC....#
#....CC...CC...CC....#
#....................#
####GG##########GG####
""".strip()

WALL = (0,0)
DOOR = (7,3)
FLOOR = (0,2)
CUSTOMER = [(3,0), (3,1), (3,2), (4,0), (4,1), (4,2), (7,0), (7,1), (7,2)]
FRUIT = [(0,4), (1,4), (2,4), (3,4), (4,4)]
VEGETABLE = [(0,11), (1,11), (2,11), (3,11), (4,11)]
DRINK = [(3,13), (0,10)]
DAIRY = [(0,-2), (1,-2)]
SPICE = [(0,3), (1,3), (2,3)]
COUNTER = (0,1)

price_dict = {
                'checkout': 0,
                'dairy': 5,
                'drinks': 6,
                'fruit': 4,
                'spices': 3
            } 


customer_per_section_dict = {
                            'checkout': 0,
                            'dairy': 0,
                            'drinks': 0,
                            'fruit': 0,
                            'spices': 0
                            }

class Section(Enum):
    checkout = 0
    dairy = 1
    drinks = 2
    fruit = 3
    spices = 4

sections = [sec.name for sec in Section]

first_section = sections[1:]


location_dict = {
                'dairy': [
                        [(2, -5), (2, -3)],
                        [(3, -5), (3, -3)],
                        [(4, -5), (4, -3)],
                        [(5, -5), (5, -3)],
                        [(6, -5), (6, -3)] 
                        ],
                'drinks': [
                        [(2, 12), (2, 14)],
                        [(3, 12), (3, 14)],
                        [(4, 12), (4, 14)],
                        [(5, 12), (5, 14)],
                        [(6, 12), (6, 14)] 
                        ],
                'fruit': [
                        [(2, 7), (2, 9)],
                        [(3, 7), (3, 9)],
                        [(4, 7), (4, 9)],
                        [(5, 7), (5, 9)],
                        [(6, 7), (6, 9)] 
                        ],
                'spices': [
                        [(2, 2), (2, 4)],
                        [(3, 2), (3, 4)],
                        [(4, 2), (4, 4)],
                        [(5, 2), (5, 4)],
                        [(6, 2), (6, 4)] 
                        ],
                'checkout': [
                        [(8, -5), (9, -5)],
                        [(8, 4), (9, 4)],
                        [(8, 7), (9, 7)],
                        [(8, 9), (9, 9)],
                        [(8, 12), (9, 12)],
                        [(8, 14), (9, 14)]
                        ],
}