# Use this code and the R objects to answer these homework questions.

x = [6,3,8,5,5,7,5,7,6,2,5,5,6,6,2,4,5,3,5,4,5,2,5,4,6,9,6,4,

       7,1,6,5,3,6,5,4,2,3,5,2,6,12,8,2,5,1,2,4,9,3,3,6,2,9,4,3,

       8,8,3,4,6,8,7,10,3,7,4,3,3,3,1,11,5,4,10,8,4,7,5,4,6,2,6,

       6,5,7,2,2,1,6,2,4,5,3,8,5,4,6,9,5,4,4,6,6,6,6,5,5,5,7,6,

       4,4,5,4,3,2,3,6,5,7,5,6,2,7,6,3,2,7,5,4,4,7,4,6,4,3,4,9,6,

       5,8,2,3,7,1,10,8,5,7,4,4,7,5,4,4,4,3,2,7,5,7,3,3,3,4,3,3,

       7,7,4,11,4,5,4,4,5,7,4,9,6,8,7,6,6,3,7,6,5,5,3,6,2,4,2,5,

       6,7,10,5,8,4,7,8,3,4,1,6,6,3,5,5,2,2,1,3,5,3,5,3,2,5,3,5,

       8,3,2,6,3,12,3,4,3,7,8,8,5,4,4,5,5,7,5,8,4,5,3,3,7,6,7,2,

       4,5,5,5,5,1,4,4,4,6,1,2,5,2,5,8,3,8,5,4,6,5,2,5,3,7,6,6,

       4,6,6,3,7,6,5,4,2,12,3,8,5,4,9,4,4,5,5,4,8,4,6,5,6,3,12,6,

       2,7,8,4,3,5,5,5,2,3,5,7,6,6,4,4,5,7,4,3,7,4,3,2,3,4,2,7,4,

       4,5,6,1,4,4,3,6,6,5,8,6,1,3,2,7,2,6,5,6,5,7,4,2,4,6,6,6,6,

       5,4,9,4,7,2,2,8,3,10,7,6,7,9,6,6,4,2,2,7,8,5,7,6,0,3,5,1,

       4,1,8,2,6,3,7,5,3,3,1,8,6,4,7,4,8,4,4,6,8,4,5,7,9,7,4,0,2,

       2,6,4,3,6,7,7,9,8,8,9,7,4,8,6,8,10,5,6,1,4,3,9,7,4,6,7,6,

       5,5,3,1,5,4,7,3,4,2,7,4,5,3,9,8,7,3,9,9,4,7,8,4,4,4,5,6,7,

       5,11,6,3,4,0,4,5,3,5,6,5,4,5,5,1,4,3,5,3]

y = x[:]

import random

random.seed(944452)

import numpy as np

z = np.random.choice(len(x), 10)
for i in z:
	y[i] = np.nan

# 1) What is the length of the x vector?
len(x)

# 2) Find the sum of the numbers in the x vector.
sum(x) # If y = x[:] is not done, this returns "nan"
# Also np.nansum(x) if there are missing values in the vector

# 3) Find the mean of the numbers in the x vector using the "mean" function
np.mean(x)

# 4) Find the mean of the numbers in the x vector using the "sum" function and 
# the definition of the mean.
sum(x) / len(x)

# 5) Find the standard deviation in the x vector.
np.std(x, ddof = 1) # ddof default is 0 (delta degrees of freedom)

# 6) Find the standard deviation of the x vector using the "sum" and "mean"
# functions and the definition of standard deviation.
#..... Not really sure how to do this normally...

# 7) Find the standard deviation of the first 50 numbers in the x vector.
np.std(x[:50], ddof = 1) # ddof default is 0

# 8) Find the sum of the numbers in the x vector whose position is even
sum(x[1::2])

# 9) Find the sum of the even numbers in the x vector.
evens = []
for i in x:
	if i % 2 == 0:
		evens.append(i)

sum(evens)