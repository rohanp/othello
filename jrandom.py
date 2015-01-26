#
# Torbert, 9 December 2014
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
   # Make this better...
   #
   sleep( 0.25 * random() )
   #
   return choice( poss )

def monteCarlo(board, player):


#
# end of file
#