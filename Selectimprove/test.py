import numpy as np
import statsmodels.api as sm
import pylab as py

# np.random generates different random numbers
# whenever the code is executed
# Note: When you execute the same code 
# the graph look different than shown below.

# Random data points generated
data_points = np.random.normal(0, 1, 100)    

sm.qqplot(data_points, line ='45')
py.show()