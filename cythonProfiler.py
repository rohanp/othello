import pstats,cProfile

import pyximport
pyximport.install()

import othelloCython

#cProfile.runctx("HybridProcessDiffusionMap.main()", {"inFileName":"modified_Met-Enk_PDBModels.pdb", "atomMode":"AA", "cutoff":.03, "nThreads":4},locals(), "Profile.prof")
cProfile.runctx('othelloCython.main')

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()