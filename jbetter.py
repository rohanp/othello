#
# Torbert, 10 December 2014
#
import reversi
#
from random import choice , random
#
from time import sleep
#
def pick( board , player ) :
   poss = reversi . get_legal_moves( board , player )
   if len(poss) == 0 :
      return None
   #
   # A little bit better...
   #
   if 11 in poss : return 11
   if 18 in poss : return 18
   if 81 in poss : return 81
   if 88 in poss : return 88
   #
   sleep( 0.25 * random() )
   #
   return choice( poss )
#
# end of file
#