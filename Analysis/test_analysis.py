
import matplotlib.pyplot as plt
import numpy as np
method ="seeded6"
i=84
file_name= ""+method+"/result"+str(i)+".txt"
f = open(file_name)
lines= f.readlines()
print(int(lines[1]))
print(int(lines[-1]))
print(int(lines[3]))
print(float(lines[5])/(float(lines[5])+float(lines[7])))
print(float(lines[9]))
f.close()