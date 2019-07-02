# Peer Review 11a

import sqlalchemy as sal
import pandas as pd

# Create the connection to the sakila database
engine = sal.create_engine('mysql://stats:stats@localhost/sakila')
connection = engine.connect()

# Read SQL table into Pandas data frame
rental = pd.read_sql('SELECT * FROM rental', con=connection)

# What is the ID number of the staff member who processed the most rentals?
rental.staff_id.value_counts() #1 

# This table tracks the rentals for a store for 3 months in 2005. Assuming each customer_id represents a different customer, what is the average number of rentals a customer bought in the 3-month span?
(rental.customer_id.value_counts()).mean() # 26.78464

# When an item is rented, how long on average does it take for that item to be returned?
(rental.return_date-rental.rental_date).mean() # 5 days, 36 min, 28 sec

 