import numpy as np
import random
from required_constants import trans, sections, Section, customer_images, fake


class Customer:
    '''Customer for the supermarket simulation'''
    def __init__(self, name: str='John Doe', trans_matrix=trans, budget: int=100, image=customer_images[0]):
        self._name = name
        self._state = None
        self._transition_matrix = trans_matrix
        self._is_active = True
        self._budget = budget
        self._image = image

    def __repr__(self) -> str:
        if self._state == None:
            return f'Customer with {self._name} is currently at the entrance'
        elif self._is_active == False:
            return f'The customer {self._name} has left the supermarket'
        else:
            return f'Customer with {self._name} is currently in {self._state}' 


    def next_state(self) -> None:
        '''
        Propagates the customer to the next state.
        '''
        if self._state == None:
            self._state = np.random.choice(a=np.array(sections), p=np.array(trans.loc['checkout']))
            return 0
        elif self._state != 'checkout':
            self._state = np.random.choice(a=np.array(sections), p=trans.loc[self._state])
        else:
            self._is_active = False



if __name__ == "__main__":

    customer1 = Customer(fake.name(), trans, 1000, random.choice(customer_images))
    customer2 = Customer(fake.name(), trans, 1000, random.choice(customer_images))
    customer3 = Customer(fake.name(), trans, 1000, random.choice(customer_images))
    customer4 = Customer()

    for customer in [customer1, customer2, customer3, customer4]:
        while customer._is_active:
            print(customer)
            customer.next_state()
