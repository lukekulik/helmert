import cProfile
import pstats
from main import main

itrf = 'ITRF/ITRF2007'
year = 'dataset/year2007'  # define year to be studied (directory in filelist)

cProfile.run('main(year,itrf)', 'restats4.txt')

p = pstats.Stats('restats4.txt')
p.sort_stats('cumulative').print_stats(15)