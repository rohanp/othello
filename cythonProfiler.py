import pstats,cProfile

import pyximport
pyximport.install()

import othelloCython

cProfile.runctx('othelloCython.main')

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()