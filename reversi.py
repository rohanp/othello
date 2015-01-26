#
# Torbert, 9 December 2014
#
black, white, empty, outer = 1, 2, 0, 3
directions = [ -11 , -10 , -9 , -1 , 1 , 9 , 10 , 11 ]
#
def bracket( board , player , square ) :
   #
   opp = opponent_color( player )
   #
   for d in directions :
      k = square + d
      if board[k] != opp :
         continue
      while board[k] == opp :
         k = k + d
      if board[k] == player :
         k = k - d
         while k != square :
            board[k] = player
            k = k - d
         #
      #
   #
#
def would_bracket( board , player , square ) :
   opp = opponent_color( player )
   for d in directions :
      k = square + d
      if board[k] != opp :
         continue
      while board[k] == opp :
         k = k + d
      if board[k] == player :
         return True

   return False
#
def get_legal_moves(board, player) :
   #
   possible = []
   #
   for row in range( 10 , 90 , 10 ) :
      for col in range( 1 , 9 ) :
         square = row + col
         if board[square] != empty :
            continue
         if would_bracket( board , player , square ) :
            possible . append( square )
         #
      #
   #
   return possible
#
def opponent_color( player ) :
   if player == black :
      return white
   return black
#
# end of file
#