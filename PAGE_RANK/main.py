import numpy as np
from numpy import matrix as mt
import panda as pd




T = mt([
    [0, 0, 1, 1/2],
    [1/3, 0, 0, 0],
    [1/3, 1/2, 0, 1/2],
    [1/3, 1/2, 0, 0],
])
p = mt([[1/4], [1/4], [1/4], [1/4]])
for i in range(100):
   p = T*p
p