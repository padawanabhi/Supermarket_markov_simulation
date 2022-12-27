##################### IMPORTS ###########################

import time
import datetime
import os
import numpy as np
import cv2
import logging
import warnings
import random
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
from customer import Customer
from required_constants import (location_dict, TILE_SIZE, trans, CUSTOMER_PRESENT_FILE, 
                            CUSTOMER_PER_SECTION, sections, customer_images, fake, 
                            customer_per_section_dict, price_dict, customer_present_df)



#####################   SUPERMARKET   #############################

    
warnings.filterwarnings("ignore")
STRT_TIME = customer_present_df.index.min()

class Supermarket:
    """manages multiple Customer instances that are currently in the market.
    """

    def __init__(self, start_time=STRT_TIME, sections=sections, image=None, locations=location_dict,
                    customer_present_table=customer_present_df, section_customer_dict=customer_per_section_dict):        
        # a list of Customer objects
        self._customers = [Customer(name = fake.name(), trans_matrix=trans, 
                                    budget=random.randint(50, 150), image=random.choice(customer_images))]
        self._current_time = start_time
        self._sections = sections
        self._original_image = image
        if self._original_image != None:
            self._temp_image = self._original_image.copy()
        else:
            self._temp_image = image
        self._locations = locations
        self._last_choice = None
        self._location_choice = None
        self._customer_present = customer_present_table
        self._customer_in_sections = section_customer_dict
        self._revenue = 0

    def __repr__(self):
        return f'There are {len(self._customers)} in the Supermarket'

    def write_customers_to_file(self) -> None:
        """print all customers with the current time and id in CSV format.
        """
        with open('./data/final_data/simulated_day.csv', 'a') as file:
            for customer in self._customers:
                if customer._is_active:
                    file.write(self._current_time, customer._name, customer._state)

    def find_and_add_customer(self):
        for customer in self._customers:
            customer.next_state()
            for section in sections:
                if section == customer._state:
                    self._location_choice = self._locations[section]
                    self._location_choice = random.choice(self._location_choice) # get the row
                    self._location_choice = random.choice(self._location_choice) # get the tuple value
                    row = self._location_choice[0]*TILE_SIZE
                    col = self._location_choice[1]*TILE_SIZE
                    self._last_choice = self._location_choice
                    if self._original_image != None:
                        self._temp_image[row:row+TILE_SIZE, col:col+TILE_SIZE] = customer._image

    def draw(self, frame):
        """
        draws the image into a frame
        """
        frame[0:self._temp_image.shape[0], 0:self._temp_image.shape[1]] = self._temp_image


    def draw_customer_per_section(self, frame):
        temp = self._customer_in_sections.copy()
        for customer in self._customers:
            if customer._state in self._customer_in_sections.keys():
                self._customer_in_sections[customer._state] += 1
                self._revenue += price_dict[customer._state]
        df = pd.DataFrame(self._customer_in_sections, index=['Customers'])
        ax = plt.subplot(1,1,1, frame_on=False)
        ax.set_xticks([])
        ax.set_yticks([])
        table(ax=ax, data=df,  cellLoc='left', colLoc='left', edges='horizontal')
        plt.savefig('./images/table.png')
        table_array = cv2.imread('./images/table.png')
        table_array = table_array[-80:, :]
        cv2.imwrite('./images/table.png', table_array)
        customer_table_image = cv2.imread('./images/table.png')
        row, col = 384, 20
        frame[row:row+customer_table_image.shape[0], col:col+customer_table_image.shape[1]] = customer_table_image
        self.write_total_revenue(frame)
        self._customer_in_sections = temp

    def write_total_revenue(self, frame):
        """
        writes info of revenue on frame
        """
        revenue_dict = {
                        'Dairy': price_dict['dairy']*self._customer_in_sections['dairy'],
                        'Drinks': price_dict['drinks']*self._customer_in_sections['drinks'],
                        'Fruit': price_dict['fruit']*self._customer_in_sections['fruit'],
                        'Spices': price_dict['spices']*self._customer_in_sections['spices'],
                        'Total': self._revenue,
                        'Current Time': self._current_time
                    
                    }
        revenue_df = pd.DataFrame(revenue_dict, index=['Amount ¢'])
        revenue_df = revenue_df.T
        ax = plt.subplot(2,1,1, frame_on=False)
        ax.set_xticks([])
        ax.set_yticks([])
        table(ax=ax, data=revenue_df, cellLoc='left', colLoc='left', edges='vertical', colWidths = [0.4])
        plt.savefig('./images/revenue.png')
        revenue_array = cv2.imread('./images/revenue.png')
        revenue_array = revenue_array[220:340, :]
        cv2.imwrite('./images/revenue.png', revenue_array)
        revenue_table_image = cv2.imread('./images/revenue.png')
        row, col = 454, 20
        frame[row:row+revenue_table_image.shape[0], col:col+revenue_table_image.shape[1]] = revenue_table_image

    
    def reset_supermarket(self):
        """
        Resets the supermarket map for the next loop.
        """
        self._temp_image = self._original_image.copy()

    def update_time(self) -> None:
        """propagates all customers to the next state.
        """
        self._current_time = self._current_time + datetime.timedelta(minutes=1)
        print(self._current_time)
        return self._current_time
    
    def add_new_customers(self) -> None:
        """randomly creates new customers.
        """
        customer_present = int(self._customer_present.loc[self._current_time][0])
        if len(self._customers) < customer_present:
            for _ in range((customer_present - len(self._customers)) + 1):
                self._customers.append(Customer(name = fake.name(), trans_matrix=trans, 
                                                budget=random.randint(50, 150), image=random.choice(customer_images)))
    

    def remove_inactive_customers(self) -> None:
        """removes every customer that is not active any more.
        """
        for customer in self._customers:
            active_list = []
            if not customer._is_active:
                active_list.remove(customer)
        self._customers = active_list

        


if __name__ == "__main__":

    background = np.zeros((584, 704, 3), np.uint8) + 255 # Make background white
    supermarket_image = cv2.imread('./images/supermarket.png')
    start_time = customer_present_df.index.min()
    supermarket = Supermarket(start_time, sections, supermarket_image,
                             location_dict, customer_present_df, customer_per_section_dict)
    print(f"start time is {start_time}")
    print(f"end time is {customer_present_df.index.max()}")

    while supermarket._current_time <= customer_present_df.index.max():
        try:
            time.sleep(1)
            frame = background.copy()
            supermarket.find_and_add_customer()
            for customer in supermarket._customers:
                print(customer)
            supermarket.draw(frame)
            supermarket.draw_customer_per_section(frame)
            supermarket.update_time()
            key = cv2.waitKey(1)
       
            if key == 113: # 'q' key
                break
            cv2.imshow("frame", frame)
            supermarket.remove_inactive_customers()
            supermarket.add_new_customers()
            supermarket.reset_supermarket()
        except KeyboardInterrupt:
            print('Simulation was stopped by user')
            break
    cv2.destroyAllWindows()