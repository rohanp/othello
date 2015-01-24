#
# Last revision... 10 December 2014
#
# Torbert, 12.2.2004
# Additions by Kassing 1.20.06
# Updated by Torbert, 1.5.2010
#
import reversi
#
from os import system
from time import time
#
def show( board , p1 , p2 , t1 , t2 , player ) :
   system('clear')
   print('Black: %s\nWhite: %s\n' % ( p1 , p2 ) )
   print('   1 2 3 4 5 6 7 8' )
   for row in range( 10 , 90 , 10 ) :
      s = str(row)
      for col in range( 1 , 9 ) :
         square = board[row + col]
         if square == reversi.empty:
            s += '\033[32;42'
         elif square == reversi.white:
            s += '\033[37;42'
         else:
            s += '\033[30;42'
         s += 'm\033[1m'
         if square == reversi.empty:
            s += '  '
         else:
            s += '* '
      print(s + '\033[0m')
   if player==reversi.black:
      print('\nBlack: %2d [%0.3f] *' % ( count(board,reversi.black) , t1 ) )
   else:
      print('\nBlack: %2d [%0.3f]  ' % ( count(board,reversi.black) , t1 ) )
   if player==reversi.white:
      print('White: %2d [%0.3f] *\n' % ( count(board,reversi.white) , t2 ) )
   else:
      print('White: %2d [%0.3f]  \n' % ( count(board,reversi.white) , t2 ) )
#
def count( board , player ) :
   total = 0
   for row in range(10, 90, 10) :
      for col in range(1, 9) :
         square = board[row + col]
         if square == player :
            total = total + 1
         #
      #
   #
   return total
#
def play_one( ht , p1 , p2 ) :
   #
   ht[p1]['time'] = 0.0
   ht[p2]['time'] = 0.0
   #
   # initialize the board...
   #
   board         = [ reversi.empty ] * 100
   board[ 0: 10] = [ reversi.outer ] * 10
   board[90:100] = [ reversi.outer ] * 10
   for k in range( 10 , 90 , 10 ) :
      board[k + 0] = reversi.outer
      board[k + 9] = reversi.outer
   board[44] , board[55] = reversi.white , reversi.white
   board[45] , board[54] = reversi.black , reversi.black
   #
   player  , pname , oname = reversi.black , p1 , p2
   squares , stuck = 4 , 0
   #
   show( board , p1 , p2 , ht[p1]['time'] , ht[p2]['time'] , player )
   #
   while squares < 64 and stuck < 2:
      #
      # make a move...
      #
      tic = time()
      square = ht[pname]['ai'] . pick( board[:] , player )
      toc = time()
      #
      ht[pname]['time'] += ( toc - tic )
      #
      # assume valid moves...
      #
      if square != None :
         board[square] = player
         reversi . bracket( board , player , square )
         squares += 1
         stuck    = 0
      else :
         stuck += 1
      #
      player = reversi . opponent_color( player )
      pname , oname = oname , pname
      #
      show( board , p1 , p2 , ht[p1]['time'] , ht[p2]['time'] , player )
      #
   #
   return [ count( board , reversi.black ) , count( board , reversi.white ) ]
   #
#
# main
#
p1 = 'jrandom'
p2 = 'jbetter'
#
ht = { p1 : {} , p2 : {} }
#
ht[p1]['ai'] = __import__( p1 )
ht[p2]['ai'] = __import__( p2 )
#
g1 = play_one( ht , p1 , p2 ) # home
g2 = play_one( ht , p2 , p1 ) # away
#
print( 'Game 1: BLACK %s (%d) WHITE %s (%d)' % ( p1 , g1[0] , p2 , g1[1] ) )
print( 'Game 2: WHITE %s (%d) BLACK %s (%d)' % ( p1 , g2[1] , p2 , g2[0] ) )
print()
#
# end of file
#