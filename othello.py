from copy import deepcopy
import numpy as np
import sys

def setUpCanvas(root): # These are the REQUIRED magic lines to enter graphics mode.
	root.title("Othello") # Your screen size may be different from 1270 x 780.
	canvas = Canvas(root, width = 1270, height = 780, bg = 'GREY30')
	canvas.pack(expand = YES, fill = BOTH)
	return canvas
#----------------------------------------------------------------------------------------------------Othello--

def createMatrix(): # = the initial position, with Black = 1, and white = -1.
	global M
	M = np.array([ [0, 0, 0, 0, 0, 0, 0, 0,],
			[0, 0, 0, 0, 0, 0, 0, 0,],
			[0, 0, 0, 0, 0, 0, 0, 0,],
			[0, 0, 0,-1, 1, 0, 0, 0,], # The matrix M is GLOBAL.
			[0, 0, 0, 1,-1, 0, 0, 0,],
			[0, 0, 0, 0, 0, 0, 0, 0,],
			[0, 0, 0, 0, 0, 0, 0, 0,],
			[0, 0, 0, 0, 0, 0, 0, 0,],])
	return M
#----------------------------------------------------------------------------------------------------Othello--

def initializePointMatrices():
	global PW, PB
##--The computer's strategy will be based off of this GLOBAL matrix, which will be modified as
#   the board configuration changes. Remember: row (going down) is first:  P[row][col]
	PW = np.array([ [1000,   50,  100,  100,  100,  100,   50, 1000,], # P[0][0], P[0][1], ..., P[0][7]
			 [  50,  -20,  -10,  -10,  -10,  -10,  -20,   50,], # P[1][0], P[1][1], ..., P[1][7]
			 [ 100,  -10,    1,    1,    1,    1,  -10,  100,], # P[2][0], P[2][1], ..., P[2][7]
			 [ 100,  -10,    1,    1,    1,    1,  -10,  100,], # P[3][0], P[3][1], ..., P[3][7]
			 [ 100,  -10,    1,    1,    1,    1,  -10,  100,], # P[4][0], P[4][1], ..., P[4][7]
			 [ 100,  -10,    1,    1,    1,    1,  -10,  100,], # P[5][0], P[5][1], ..., P[5][7]
			 [  50,  -20,  -10,  -10,  -10,  -10,  -20,   50,], # P[6][0], P[6][1], ..., P[6][7]
			 [1000,   50,  100,  100,  100,  100,   50, 1000,],])# P[7][0], P[7][1], ..., P[7][7]
	from copy import deepcopy
	PB = PW.copy()
	return PW, PB
#----------------------------------------------------------------------------------------------------Othello--

def updateTheFourCorners(M, PW, PB):
#---1B. Modify upper-left corner cell's values if the HUMAN has taken that corner.
	if M[0][0] == 1:
		PW[0][1] = -50
		PW[1][0] = -200
		PW[1][1] = -50
		PB[0][1] = 100
		PB[1][0] = 100
		PB[1][1] = 100

#---2B. Modify upper-right corner cell's values if the HUMAN has taken that corner.
	if M[0][7] == 1:
		PW[0][6] = -50
		PW[1][7] = -200
		PW[1][6] = -50
		PB[0][6] = 100
		PB[1][7] = 100
		PB[1][6] = 100

#---3B. Modify lower-left corner cell's values if the HUMAN has taken that corner.
	if M[7][0] == 1:
		PW[6][0] = -50
		PW[6][1] = -200
		PW[7][1] = -50
		PB[6][0] = 100
		PB[6][1] = 100
		PB[7][1] = 100

#---4B. Modify lower-right corner cell's values if the HUMAN has taken that corner.
	if M[7][7] == 1:
		PW[7][6] = -50
		PW[6][7] = -200
		PW[6][6] = -50
		PB[7][6] = 100
		PB[6][7] = 100
		PB[6][6] = 100

#---1W. Modify upper-left corner cell's values if the COMPUTER has taken that corner.
	if M[0][0] == -1:
		PW[0][1] = 100
		PW[1][0] = 100
		PW[1][1] = 100
		PB[0][1] = -50
		PB[1][0] = -200
		PB[1][1] = -50

#---2W. Modify upper-right corner cell's values if the COMPUTER has taken that corner.
	if M[0][7] == -1:
		PW[0][6] = 100
		PW[1][7] = 100
		PW[1][6] = 100
		PB[0][6] = -50
		PB[1][7] = -200
		PB[1][6] = -50

#---3W. Modify lower-left corner cell's values if the COMPUTER has taken that corner.
	if M[7][0] == -1:
		PW[6][0] = 100
		PW[6][1] = 100
		PW[7][1] = 100
		PB[6][0] = -50
		PB[6][1] = -200
		PB[7][1] = -50

#---4W. Modify lower-right corner cell's values if the COMPUTER has taken that corner.
	if M[7][7] == -1:
		PW[7][6] = 100
		PW[6][7] = 100
		PW[6][6] = 100
		PB[7][6] = -50
		PB[6][7] = -200
		PB[6][6] = -50

	return PW, PB
#----------------------------------------------------------------------------------------------------Othello--

def updateTheMiddleRowsAndColumns(M, PW, PB):
	for n in range (2, 6):
		if M[0][n] == -1:
			PW[1][n] =  20 # TOP    row
			PB[1][n] = -10 # TOP    row
		if M[7][n] == -1:
			PW[6][n] =  20 # BOTTOM row
			PB[6][n] = -10 # BOTTOM row
		if M[n][0] == -1:
			PW[n][1] =  20 # LEFT  column
			PB[n][1] = -10 # LEFT  column
		if M[n][7] == -1:
			PW[n][6] =  20 # RIGHT column
			PB[n][6] = -10 # RIGHT column
		if M[0][n] == 1:
			PW[1][n] = -10 # TOP    row
			PB[1][n] =  20 # TOP    row
		if M[7][n] == 1:
			PW[6][n] = -10 # BOTTOM row
			PB[6][n] =  20 # BOTTOM row
		if M[n][0] == 1:
			PW[n][1] = -10 # LEFT  column
			PB[n][1] =  20 # LEFT  column
		if M[n][7] == 1:
			PW[n][6] = -10 # RIGHT column
			PB[n][6] =  20 # RIGHT column
	return PW, PB
#----------------------------------------------------------------------------------------------------Othello--

def UpdateThePointMatrices():
	updateTheFourCorners(M, PW, PB)
	updateTheMiddleRowsAndColumns(M, PW, PB)
#----------------------------------------------------------------------------------------------------Othello--

def copyMatrixToScreen():
	canvas.create_text(30,30, text="x", fill = 'BLACK', font = ('Helvetica',1))
	for r in range (8):
		for c in range (8):
			if M[r][c] == 1:
				sx = c*70 + 85
				sy = r*70 + 105
				canvas.create_oval(sx-25,sy-25, sx+25, sy+25, fill = 'BLACK')
			if M[r][c] == -1:
				sx = c*70 + 85
				sy = r*70 + 105
				canvas.create_oval(sx-25,sy-25, sx+25, sy+25, fill = 'WHITE')
	canvas.update()
#----------------------------------------------------------------------------------------------------Othello--

def copyOldBoardToScreenInMiniturizedForm(rr, cc):
 #--erase previous miniture board
	canvas.create_rectangle(650, 400, 821, 567, width = 5, fill    = 'GRAY30')
	ch = chr(9679)
	for r in range (8):
		for c in range (8):
			sx = c*20 + 665
			sy = r*20 + 412
			if M[r][c] ==  1:
				 canvas.create_text(sx, sy, text = ch, fill = 'BLACK', font = ('Helvetica', 20, 'bold') )
			if M[r][c] == -1:
				 canvas.create_text(sx, sy, text = ch, fill = 'WHITE', font = ('Helvetica', 20, 'bold') )
	canvas.create_text(cc*20 + 665, rr*20 + 413, text = 'B', fill = 'BLACK', font = ('Helvetica', 9, 'bold') )
	canvas.update()
#----------------------------------------------------------------------------------------------------Othello--
#----------------------------------------------------------------------------------------------------Othello--

def LocateTurnedPieces(r, c, player, M): # The pieces turned over are of -player's color. A zero in a
	if M[r][c] != 0: return []        # matrix M cell means an empty cell. This function does NOT
	totalFlipped =   []               # turn any pieces over.
 #--case 1 (move right)
	flipped = []
	if c < 6 and M[r][c+1] == -player:
		for n in range(1, 9):
			if c+n > 7 or M[r][c+n] == 0:
				flipped = []
				break
			if M[r][c+n] == player: break
			flipped += ((r,c+n,),)  # <-- We save the cell locations as tuples.
	totalFlipped += flipped


 #--case 2 (move down)
	flipped = []
	if r < 6 and M[r+1][c] == -player:
		for n in range(1, 9):
			if r+n > 7 or M[r+n][c] == 0:
				flipped = []
				break
			if M[r+n][c] == player: break
			flipped += ((r+n,c,),)
	totalFlipped += flipped

 #--case 3 (move up)
	flipped = []
	if r > 1 and M[r-1][c  ] == -player:
		for n in range(1, 9):
			if r-n < 0 or M[r-n][c] == 0:
				flipped = []
				break
			if M[r-n][c] == player: break
			flipped += ((r-n,c,),)
	totalFlipped += flipped

 #--case 4 (move left)
	flipped = []
	if c > 1 and M[r][c-1] == -player:
		for n in range(1, 9):
			if c-n < 0 or M[r][c-n] == 0:
				flipped = []
				break
			if M[r][c-n] == player: break
			flipped += ((r,c-n,),)
	totalFlipped += flipped

 #--case 5 (move down and right)
	flipped = []
	if r < 6 and c < 6 and M[r+1][c+1] == -player:
		for n in range(1, 9):
			if (r+n) > 7 or (c+n) > 7 or M[r+n][c+n] == 0:
				flipped = []
				break
			if M[r+n][c+n] == player: break
			flipped += ((r+n,c+n,),)
	totalFlipped += flipped

 #--case 6 (move up and left)
	flipped = []
	if r > 0 and c > 0 and M[r-1][c-1] == -player:
		for n in range(1, 9):
			if (r-n) < 0 or (c-n) < 0 or M[r-n][c-n] == 0:
				flipped = []
				break
			if M[r-n][c-n] == player: break
			flipped += ((r-n,c-n,),)
	totalFlipped += flipped

#--case 7 (move up and right)
	flipped = []
	if r > 1 and c < 6 and M[r-1][c+1] == -player:
		for n in range(1, 9):
			if (r-n) < 0 or (c+n) > 7 or M[r-n][c+n] == 0:
				flipped = []
				break
			if M[r-n][c+n] == player: break
			flipped += ((r-n,c+n,),)
	totalFlipped += flipped



 #--case 8 (move down and left)
	flipped = []
	if r < 6 and c > 1 and M[r+1][c-1] == -player:
		for n in range(1, 9):
			if (r+n) > 7 or (c-n) < 0 or M[r+n][c-n] == 0:
				flipped = []
				break
			if M[r+n][c-n] == player: break
			flipped += ((r+n,c-n,),)
	totalFlipped += flipped

	return totalFlipped
#----------------------------------------------------------------------------------------------------Othello--

def setUpInitialBoard(canvas):
	global M; ch = chr(9679)

 #--print title
	canvas.create_text(330, 50, text = "OTHELLO with AI", \
						 fill = 'WHITE',  font = ('Helvetica', 20, 'bold'))
 #--print directions
	stng = "DIRECTIONS:\n1) Black (human) moves first. Click on any unoccupied cell.\n\
2) If a player cannot move, play passes to the opponent. \n3) Game ends when \
no legal move is possible.\n4) The player with the most colors on the board \
wins.\n5) A legal move MUST cause some pieces to turn color."
	canvas.create_text(810, 100, text = stng,  \
						 fill = 'WHITE',  font = ('Helvetica', 10, 'bold'))
 #--draw outer box, with red border
	canvas.create_rectangle(50, 70, 610, 630, width = 1, fill    = 'DARKGREEN')
	canvas.create_rectangle(47, 67, 612, 632, width = 5, outline = 'RED'  )

 #--Draw 7 horizontal and 7 vertical lines to make the cells
	for n in range (1, 8): # draw horizontal lines
		 canvas.create_line(50, 70+70*n, 610, 70+70*n, width = 2, fill = 'BLACK')
	for n in range (1, 8):# draw vertical lines
		 canvas.create_line(50+70*n,  70, 50+70*n, 630, width = 2, fill = 'BLACK')

 #--Place gold lines to indicate dangerous area to play (optional).
	canvas.create_rectangle(47+73, 67+73, 612-73, 632-73, width = 1, outline = 'GOLD'  )
	canvas.create_rectangle(47+2*71, 67+2*71, 612-2*71, 632-2*71, width = 1, outline = 'GOLD'  )

 #--Place letters at bottom
	tab = " " * 7
	stng = 'a' + tab + 'b' + tab + 'c' + tab + 'd' + tab + 'e' + \
				 tab + 'f' + tab + 'g' + tab + 'h'
	canvas.create_text(325, 647, text = stng, fill = 'DARKBLUE',  font = ('Helvetica', 20, 'bold'))

 #--Place digits on left side
	for n in range (1,9):
		canvas.create_text(30, 35 + n * 70, text = str(n),
						 fill = 'DARKBLUE',  font = ('Helvetica', 20, 'bold'))
 #--copy matrix to screen.
	copyMatrixToScreen()

 #--Place score on screen
	(BLACK, WHITE) = score(M)
	stng = 'BLACK = ' + str(BLACK) + '\nWHITE  = ' + str(WHITE)
	canvas.create_text(800, 200, text = stng, fill = 'WHITE',  font = ('Helvetica', 20, 'bold'))
	stng = "Suggested reply (col, row): (c, 4)"
	canvas.create_text     (755,350,text = stng, fill = 'GREEN',  font = ('Helvetica', 10, 'bold'))
#----------------------------------------------------------------------------------------------------Othello--


def illegalClick(x, y): # Click is not on board or click is on an already-filled cell.
	player = 1 # player = Black
	if x < 52 or x > 609:
		print("Error 1. Mouse is to left or right of board.")
		return True # = mouse position is off the board

	if y < 62 or y > 632:
		print("Error 2.Mouse is above or below the board.")
		return True # = mouse position is off the board

 #--Calculate matrix position
	c = (x-50)//70
	r = (y-70)//70

	if M[r][c] != 0:
		print("ERROR 3: Cell is occupied at r =", r, " c =", c)
		return True      # = cell is occupied

 #--Not next to cell of opposite color
	flag = 0
	if c < 7 and           M[r  ][c+1] == -player: return False
	if r < 7 and           M[r+1][c  ] == -player: return False
	if r > 0 and           M[r-1][c  ] == -player: return False
	if c > 0 and           M[r  ][c-1] == -player: return False
	if r < 7 and c < 7 and M[r+1][c+1] == -player: return False
	if r > 0 and c > 0 and M[r-1][c-1] == -player: return False
	if r > 0 and c < 7 and M[r-1][c+1] == -player: return False
	if r < 7 and c > 0 and M[r+1][c-1] == -player: return False
	print("ERROR 4: no opposite colored neighbors at r =", r, " c =", c)
	return True # = illegal move
#----------------------------------------------------------------------------------------------------Othello--

def legalMove(player): # Check to see if any pieces will be turned over.
	pieces = []
	for r in range(8):
		for c in range(8):
			 pieces += LocateTurnedPieces(r, c, player, M)
		if pieces != []: break
	if pieces ==[]:
		 person = 'WHITE'
		 if player == 1: person = 'BLACK'
		 stng = 'There is no legal move for ' + person
		 canvas.create_rectangle(655,260,957,307, width = 0, fill = 'GRAY30')
		 canvas.create_text     (800,280,text = stng, fill = 'RED',  font = ('Helvetica', 10, 'bold'))
		 return False
	return True
#----------------------------------------------------------------------------------------------------Othello--

def score(M): # returns the number of black disks and white disks.
	whiteTotal = 0; blackTotal = 0
	for r in range(8):
		for c in range (8):
			if M[r][c] ==  1: blackTotal += 1
			if M[r][c] == -1: whiteTotal += 1
	return (blackTotal, whiteTotal)

def makeMove(r, c, pieces, player):
	if player not in [1, -1]: exit('ERROR: BAD PLAYER'+ str(player))
 #--make the player's legal move in matrix
	M[r][c] = player

 #--flip pieces to same color as the player
	for elt in pieces:
		M[elt[0]][elt[1]] = player

#--update the screen
	copyMatrixToScreen()

 #--erase old score and previous move
	canvas.create_rectangle(650, 160, 960, 310, width = 5, fill = 'GRAY30')

 #--print new score
	(BLACK, WHITE) = score(M)
	stng = 'BLACK = ' + str(BLACK) + '\nWHITE  = ' + str(WHITE)
	canvas.create_text(800, 200, text = stng, \
						 fill = 'WHITE',  font = ('Helvetica', 20, 'bold'))

 #--print previous move on miniture board
	position = "previous move: "+ str(chr(c + 97))+str(r+1)
	canvas.create_text(800, 250, text = position, \
						 fill = 'WHITE',  font = ('Helvetica', 20, 'bold'))

	if player == COMPUTER:
		 canvas.create_text(c*20 + 665, r*20 + 413, text = 'W', fill = 'WHITE', \
							 font = ('Helvetica', 9, 'bold') )
	return M
#----------------------------------------------------------------------------------------------------Othello--
def quit():
	canvas.create_text(330, 350, text = "GAME OVER", \
						 fill = 'RED',  font = ('Helvetica', 40, 'bold'))
	stng = 'THERE ARE NO LEGAL MOVES FOR EITHER PLAYER.'
	canvas.create_rectangle(655, 260, 955, 300, width = 0, fill = 'GRAY30')
	canvas.create_text(805, 280, text = stng, fill = 'GOLD',  font = ('Helvetica', 9, 'bold'))
#----------------------------------------------------------------------------------------------------Othello--

def pointsGained(player, r,c, pieces):
	if player == COMPUTER:
		 total = PW[r][c]          # total = the points associated with the piece played on the board.
		 for (rr,cc) in pieces:
			 total += 2*PW[rr][cc] # Add the values associated with the flipped pieces.
		 return total
	if player == HUMAN:
		 total = PB[r][c]          # total = the points associated with the piece played on the board.
		 for (rr,cc) in pieces:
			 total += 2*PB[rr][cc] # Add the values associated with the flipped pieces.
		 return total
	exit('ERROR in pointsGained() player = ' + str(player))
#----------------------------------------------------------------------------------------------------Othello--

def computerGame():
 #--Make human move(s) and computer reply/replies.
	copyOldBoardToScreenInMiniturizedForm(c,r)
	move=minimax()
	makeMove(move[1], move[0], move[2], COMPUTER)
	canvas.create_rectangle(655, 330, 870,370, width = 0, fill = 'grey30')

	if legalMove(HUMAN) and not legalMove(COMPUTER): return

 #--Make computer reply/replies (1 = BLACK = human, -1 = computer = WHITE)
	if legalMove(COMPUTER): makeComputerReply() # <--This is the computer's strategy (IMPORTANT!).
	while legalMove(COMPUTER) and not legalMove(HUMAN):
		makeComputerReply()
	#displayAllLegalMovesForHumanPlayer('BLACK')

	if not legalMove(HUMAN) and not legalMove(COMPUTER): quit()
 #-- Note: legal move for human must now necessarily exist.
	return

def makeComputerReply():
	UpdateThePointMatrices()
	move=minimax(COMPUTER)
	makeMove(move[0], move[1], move[2], COMPUTER)
	displayAllLegalMovesForHumanPlayer('BLUE')

#   printBestPotentialReply(COMPUTER) # <--Optional feature

def minimax(player):
	moves=getMoves(player, M)
	scores = np.zeros(len(moves))
	alpha = float("-inf")
	beta = float("inf")

	for i, move in enumerate(moves):
		boardCopy = fakeMove(move[0], move[1], move[2], COMPUTER, np.copy(M))
		scores[i]=maxMove(boardCopy, 1, alpha, beta, PW, PB)

	maxIndex=np.argmax(scores)
	return moves[maxIndex]

def maxMove(board, depth, alpha, beta, PW, PB):
	moves=getMoves(COMPUTER,board)
	scores=np.zeros(len(moves))

	if len(moves)==0:
		if depth<=MAXDEPTH:
			return minMove(board, depth+1, alpha, beta, PW, PB)
		else: return boardScore(board, PW, PB)

	for i, move in enumerate(moves):
		boardCopy = fakeMove(move[0], move[1], move[2], COMPUTER, np.copy(board))
		PW, PB = updateTheFourCorners(boardCopy, PW, PB)
		PW, PB = updateTheMiddleRowsAndColumns(boardCopy, PW, PB)
		if depth>=MAXDEPTH:
			scores[i] = boardScore(boardCopy, PW, PB)

		else:
			scores[i] = minMove(boardCopy, depth+1, alpha, beta, PW, PB)
			if scores[i] > alpha:
				alpha = scores[i]
			if beta <= alpha:
				#print("PRUNED")
				return scores[i]

	return max(scores)

def minMove(board, depth, alpha, beta, PW, PB):
	moves=getMoves(HUMAN,board)
	scores=np.zeros(len(moves))

	if len(moves)==0:
		if depth<=MAXDEPTH:
			return maxMove(board, depth+1, alpha, beta, PW, PB)
		else: return boardScore(board, PW, PB)

	for i, move in enumerate(moves):
		boardCopy = fakeMove(move[0], move[1], move[2], HUMAN, np.copy(board))
		PW, PB = updateTheFourCorners(boardCopy, np.copy(PW), np.copy(PB))
		PW, PB = updateTheMiddleRowsAndColumns(boardCopy, PW, PB)
		if depth>=MAXDEPTH:
			scores[i] = boardScore(boardCopy, PW, PB)
		else:
			scores[i] = maxMove(boardCopy, depth+1, alpha, beta, PW, PB)
			if beta > scores[i]:
				beta = scores[i]
			if beta <= alpha:
				#print("PRUNED")
				return scores[i]

	return min(scores)

def getMoves(player, M):
	moves=[]
	for r in range(0,8):
		for c in range(0,8):
			if M[r][c]==0:
				piecesTurned= LocateTurnedPieces(r, c, player, M)
				if len(piecesTurned)!=0:
					moves.append((r,c,piecesTurned))
	return moves

def boardScore(M, PW, PB): # The higher the boardScore, the better for the COMPUTER.
	computerTotal = 0
	humanTotal    = 0

	for r in range(0, 8):
		for c in range(0, 8):
			if M[r][c] == COMPUTER:
				computerTotal += PW[r][c]
			if M[r][c] == HUMAN:
				humanTotal += PB[r][c]
	return  computerTotal - humanTotal

def boardScore2(M, PW, PB):
	computerTotal=sum([[PW[r][c] if M[r][c] is COMPUTER else PB[r][c] for c in range(0,8)]  for r in range(0,8)])

def fakeMove(r, c, piecesTurnedOver, player, M):
#---Double check that our move is made to an empty cell.
	assert M[r][c] == 0, ['player =', str(player)]

#---Make the move
	M[r][c] = player

#---Double check that the pieces we are turning over are of the opposite color of our player.
	piecesAreOppositeColorOfPlayer = True
	for (r,c) in piecesTurnedOver:
		if M[r][c] == player:
		   piecesAreOppositeColorOfPlayer = False

	if(piecesAreOppositeColorOfPlayer==False):
		print("\n\n")
		print(M,r,c,piecesTurnedOver)
	assert piecesAreOppositeColorOfPlayer == True

#---Turn the pieces over.
	for (r,c) in piecesTurnedOver:
		M[r][c] = player
	return M
#----------------------------------------------------------------------------------------------------Othello--

def displayAllLegalMovesForHumanPlayer(kolor):
	for r in range(0, 8):
		for c in range(0, 8):
			sy = r*70 + 109
			sx = c*70 + 85
			if M[r][c] == 0: # an empty cell contains a zero integer.
				total  = len(LocateTurnedPieces(r, c, HUMAN, M))
				canvas.create_oval(sx-25,sy-25, sx+25, sy+25, fill = 'DARKGREEN', outline='DARKGREEN')

			if M[r][c] == 0 and total != 0:
				canvas.create_oval(sx-25,sy-25, sx+25, sy+25, fill = 'DARKGREEN', outline='DARKGREEN')
				canvas.create_text( sx, sy, text = str(total), fill = kolor, font = ('Helvetica', 20, 'bold') )
#----------------------------------------------------------------------------------------------------Othello--

def click(evt): # A legal move is guaranteed to exist.
	displayAllLegalMovesForHumanPlayer('BLUE')

 #--If move is off board, or cell full, or no opp. neighbor, then CLICK AGAIN.
	if illegalClick(evt.x, evt.y):
		canvas.create_rectangle(660, 270, 940,300, width = 0, fill = 'GRAY30')
		stng = 'Your last mouse click was an ILLEGAL MOVE.'
		canvas.create_text(800, 280, text = stng, fill = 'RED',  font = ('Helvetica', 9, 'bold'))
		return

 #--Find matrix coordinates (c,r) in terms of mouse coordinates (evt.x, evt.y).
	c = (evt.x-50)//70
	r = (evt.y-70)//70

 #--if none of the computer's pieces will be turned, then CLICK AGAIN.
	pieces     = LocateTurnedPieces(r, c, HUMAN, M)
	if pieces == []:
		 canvas.create_rectangle(660, 270, 940,300, width = 0, fill = 'GRAY30')
		 stng = 'Your last mouse click did NOT turn a piece.'
		 canvas.create_text(800, 280, text = stng, fill = 'ORANGE',  font = ('Helvetica', 9, 'bold'))
		 return

 #--Make human move(s) and computer reply/replies.
	copyOldBoardToScreenInMiniturizedForm(c,r)
	makeMove(r, c, pieces, HUMAN)
	canvas.create_rectangle(655, 330, 870,370, width = 0, fill = 'grey30')
	if legalMove(HUMAN) and not legalMove(COMPUTER): return

 #--Make computer reply/replies (1 = BLACK = human, -1 = computer = WHITE)
	if legalMove(COMPUTER): makeComputerReply() # <--This is the computer's strategy (IMPORTANT!).
	while legalMove(COMPUTER) and not legalMove(HUMAN):
		makeComputerReply()
	#displayAllLegalMovesForHumanPlayer('BLACK')

	if not legalMove(HUMAN) and not legalMove(COMPUTER): quit()
 #-- Note: legal move for human must now necessarily exist.
	return
#----------------------------------------------------------------------------------------------------Othello--

def bestHumanResponse():
	UpdateThePointMatrices()
#--Make a move that picks up the most points using the point matrix (PB).
	bestRow = -1
	bestCol = -1
	maxTotal = float('-inf')
	for r in range(0, 8):
		for c in range(0, 8):
			if M[r][c] == 0:
				pieces = LocateTurnedPieces(r, c, HUMAN, M)
				if len(pieces) == 0:
					continue
				total = pointsGained(HUMAN, r, c, pieces)
				print
				if maxTotal < total:
				 maxTotal = total
				 bestRow = r
				 bestCol = c
				 finalPieces = pieces
	return maxTotal, bestRow, bestCol

#===================================<GLOBAL CONSTANTS and GLOBAL IMPORTS>=====================================

# Global Variables should be avoided. But in Python's Tk graphics this is impossible.
from tkinter  import *   # <-- Use Tkinter in Python 2.x
root     =  Tk()
canvas   =  setUpCanvas(root)
PW, PB   =  initializePointMatrices()
M        =  createMatrix() # <-- No variable can be passed to the click function.
HUMAN    =  1 # = Black
COMPUTER = -1 # = White
GLOBAL   = True
MAXDEPTH = int(sys.argv[1])
#====================================================<MAIN>===================================================

def main():
	root.bind('<Button-1>', click) # 1 = LEFT  mouse button.
	root.bind('<Button-3>', click) # 3 = RIGHT mouse button.
	setUpInitialBoard(canvas)
	#computerGame()
	root.mainloop()                # Now the graphics window waits for the click function to be called.
#----------------------------------------------------------------------------------------------------Othello--
if __name__ == '__main__':  main()