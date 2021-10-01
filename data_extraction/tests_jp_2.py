import glob
import os

files = glob.glob(os.getcwd() + '/data/*.csv')


for file in files:
    print(file)