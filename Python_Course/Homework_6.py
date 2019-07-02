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
mtcars[mtcars['mpg'] == max(mtcars['mpg'])]
# Toyota Corolla -- "cyl"=4.0 and "gear"=4.0

# Find the frequency of the number of carburetors ("carb" variable) for this sample of cars and sort these values by the least frequent to the most frequent.
mtcars.carb.value_counts(ascending=True)

# The index for this data frame is currently set to the car make and model. Temporarily change the index to its default.
mtcars.reset_index()

# The "am" variable contains a 0 for a car with automatic transmission and a 1 for a car with manual transmission. Using 1 line of code, find the minimum and maximum horsepower ("hp" variable) for both a car with automatic transmission and a car with manual transmission out of these sample of cars. (Should return 4 values)
mtcars.groupby('am').agg({'hp' :['min', 'max']})

# Create a histogram that shows the number of cars for each interval of miles per gallon. Your histogram should contain 5 intervals between 10 and 35 miles per gallon. Refer to this link for the parameters of the Matplotlib histogram function.
import matplotlib.pyplot as plt
mtcars.mpg.hist(bins=5, range=(10,35))
plt.show()