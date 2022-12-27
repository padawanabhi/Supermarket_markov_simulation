import random
import pytest
import pandas as pd
import numpy as np
from required_constants import fake, trans, sections, customer_images
from customer import Customer
from supermarket_simulater import Supermarket


class TestDefaultCustomer():
    CUST = Customer()

    def test_setup(self):
        assert isinstance(self.CUST, Customer)

    def test_name(self):
        assert isinstance(self.CUST._name, str)

    def test_trans_matrix(self):
        assert isinstance(self.CUST._transition_matrix, pd.DataFrame)
    
    def test_budget(self):
        assert self.CUST._budget == 100

    def test_image(self):
        assert isinstance(self.CUST._image, np.ndarray)


class TestNewCustomer(TestDefaultCustomer):
    CUST = Customer(name=fake.name(), trans_matrix=trans, budget=100, image=random.choice(customer_images))


class TestSupermarket():
    SPRMKT = Supermarket()

    def test_setup(self):
        assert isinstance(self.SPRMKT, Supermarket)

    def test_supermarket_simulation(self):
        while self.SPRMKT._current_time < self.SPRMKT._customer_present.index.max():
            self.SPRMKT.find_and_add_customer()
            self.SPRMKT.update_time()
            self.SPRMKT.remove_inactive_customers()
            self.SPRMKT.add_new_customers()
