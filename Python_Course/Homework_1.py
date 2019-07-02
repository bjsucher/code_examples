# Load the mtcars dataset that comes preinstalled in R.
from rpy2.robjects import r, pandas2ri
def data(name):
	return pandas2ri.ri2py(r[name]) # Put at top of homework
	
mtcars = data('mtcars')

# Find the mean of the miles per gallon variable.
import numpy as np # Put at top of homework
np.mean(mtcars['mpg'])

mpg = np.array(mtcars['mpg'])
mpg.mean()

# Compute the linear correlation between the "mpg" and "cyl" variables.
import pandas as pd
mtcars = pd.DataFrame(mtcars)
mtcars['mpg'].corr(mtcars['cyl'])

# Compute the linear correlation between the "mpg" and "gear" variables.
mtcars['mpg'].corr(mtcars['gear'])

# Find the mean of the "mpg" variable for each value of the "gear" variable.
mtcars.groupby('gear').mean()

# Find the median of the "mpg" variable for each value of the "gear" variable.
mtcars.groupby('gear').median()

# Find the make and model of the car with the highest miles per gallon. What
# are its "cyl" and "gear" values?
