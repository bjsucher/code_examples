import statsmodels.api as sm
import pandas as pd

# Read in the data
longley = pd.read_csv('longley.csv')

# Set X to be explanatory variables
X = longley[["GNP.deflator", "GNP", "Unemployed", "Armed.Forces", "Population", "Year"]]

# Set y to be response variable
y = longley['Employed']

# Adds the constant/intercept for regression analysis
X_1 = sm.add_constant(X)

# Run the regression analysis and get the summary
model = sm.OLS(y, X_1).fit()
print(model.summary())

exit()
