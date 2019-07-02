# Peer Review 11b

import sqlalcehmy as sal
import pandas as pd

# Create Pandas data frame movies
movies = pd.DataFrame({'movie': ['Pirates of the Caribbean', 'The Hunger Games', 'The Greatest Showman', 'Inception', 'Harry Potter and the Goblet of Fire'], 'year': [2003, 2012, 2017, 2010, 2005]})

# Create connection to MySQL database sakila
engine = sal.create_engine('mysql://stats:stats@localhost/sakila')

# Import table into MySQL database sakila
movies.to_sql(name='movies', con=engine, index=False)
  