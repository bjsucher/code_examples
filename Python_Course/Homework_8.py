# Correct code for reproducing ggplot2 graph. 
import math, #datetime
import rpy2.robjects as ro
from rpy2.robjects import r
r('library(ggplot2)') # Might be optional
import rpy2.robjects.lib.ggplot2 as ggplot2
from rpy2.robjects.packages import importr
base = importr('base')
datasets = importr('datasets')
mtcars = datasets.__rdata__.fetch('mtcars')['mtcars']
pp = ggplot2.ggplot(mtcars) + \
     ggplot2.aes_string(x='wt', y='mpg', col='factor(cyl)') + \
     ggplot2.geom_point() + \
     ggplot2.geom_smooth(ggplot2.aes_string(group = 'cyl'),
                         method = 'lm')
pp.plot()