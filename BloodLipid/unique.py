import sys
sys.path.append('..')
import random
from my_utils import *
import matplotlib.pyplot as plt

files=(get_files(".", in_file="res"))
for e in files:
    print(get_distinct_from_res(e))