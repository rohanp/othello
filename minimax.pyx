import numpy as np
cimport numpy as np
from cython.view cimport array as cvarray

DTYPE = np.int16
ctypedef np.int16_t DTYPE_t

HUMAN=1
COMPUTER=-1

def minimax(player, M, PW, PB, MAXDEPTH):
	return passValues(player, M, PW, PB, MAXDEPTH)

cdef passValues(player, M, PW, PB, MAXDEPTH):
	cdef DTYPE_t[:,:] M_view = np.array(M, dtype=DTYPE)
	cdef DTYPE_t[:,:] PW_view = np.array(PW, dtype=DTYPE)
	cdef DTYPE_t[:,:] PB_view = np.array(PB, dtype=DTYPE)
	cdef DTYPE_t[:] scores
	cdef tuple[:,:] moves
	cdef DTYPE_t[:,:] boardCopy
	cdef int i

	moves = getMoves(player, M_view)
	scores = np.zeros(len(moves), dtype=DTYPE)
	alpha = float("-inf")
	beta = float("inf")

	for i, move in enumerate(moves):
		boardCopy = M_view[:,:]
		boardCopy = fakeMove(move[0], move[1], LocateTurnedPieces(move[0], move[1], COMPUTER, boardCopy), COMPUTER, M_view[:,:])
		scores[i]=maxMove(boardCopy, 1, alpha, beta, PW_view, PB_view, MAXDEPTH)

	maxIndex=np.argmax(scores)
	return moves[maxIndex]

cdef maxMove(DTYPE_t[:,:] board, depth, alpha, beta, DTYPE_t[:,:] PW, DTYPE_t[:,:] PB, MAXDEPTH):
	cdef tuple[:,:] moves_view
	cdef DTYPE_t[:,:] boardCopy
	cdef int i

	moves = getMoves(HUMAN,board)

	if(moves.ndim>1):
		moves_view=moves
	else:
		return boardScore(board,PW,PB)

	cdef DTYPE_t[:] scores=np.zeros(moves.shape[0], dtype=DTYPE)

	if len(moves)==0:
		if depth<MAXDEPTH:
			return minMove(board, depth+1, alpha, beta, PW, PB, MAXDEPTH)
		else: return boardScore(board, PW, PB)

	for i, move in enumerate(moves):
		boardCopy=board.copy()
		boardCopy= fakeMove(move[0], move[1], LocateTurnedPieces(move[0], move[1], COMPUTER, boardCopy) , COMPUTER, boardCopy)
		if depth>=MAXDEPTH:
			scores[i] = boardScore(boardCopy, PW, PB)
		else:
			scores[i] = minMove(boardCopy, depth+1, alpha, beta, PW, PB, MAXDEPTH)
			if scores[i] > alpha:
				alpha = scores[i]
			if beta <= alpha:
				return scores[i]


	return max(scores)

cdef minMove(DTYPE_t[:,:] board, int depth, float alpha, float beta, DTYPE_t[:,:]PW, DTYPE_t[:,:]PB, MAXDEPTH):
	cdef tuple[:,:] moves_view
	cdef DTYPE_t[:,:] boardCopy
	cdef int i

	moves = getMoves(HUMAN,board)

	if(moves.ndim>1):
		moves_view=moves
	else:
		return boardScore(board,PW,PB)

	cdef DTYPE_t[:] scores=np.zeros(moves.shape[0], dtype=DTYPE)

	if moves.shape[0]==0:
		if depth<MAXDEPTH:
			return maxMove(board, depth+1, alpha, beta, PW, PB, MAXDEPTH)
		else: return boardScore(board, PW , PB)

	for i, move in enumerate(moves_view):
		boardCopy=board.copy()
		boardCopy = fakeMove(move[0], move[1], LocateTurnedPieces(move[0], move[1], HUMAN, boardCopy), HUMAN, boardCopy)
		if depth>=MAXDEPTH:
			scores[i] = boardScore(boardCopy, PW, PB)
		else:
			scores[i] = maxMove(boardCopy, depth+1, alpha, beta, PW, PB, MAXDEPTH)
			if beta > scores[i]:
				beta = scores[i]
			if beta <= alpha:
				return scores[i]

	return min(scores)

cdef boardScore(DTYPE_t[:,:] M, DTYPE_t[:,:] PW, DTYPE_t[:,:] PB): # The higher the boardScore, the better for the COMPUTER.
	cdef int r,c,computerTotal,humanTotal
	computerTotal = 0
	humanTotal    = 0

	for r in range(0, 8):
		for c in range(0, 8):
			if M[r][c] == COMPUTER:
				computerTotal += PW[r][c]
			if M[r][c] == HUMAN:
				humanTotal += PB[r][c]
	return  computerTotal - humanTotal

cdef fakeMove(r, c, piecesTurnedOver, player, DTYPE_t[:,:] M):
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

cdef getMoves(player, DTYPE_t[:,:] M):
	moves=[]
	for r in range(0,8):
		for c in range(0,8):
			if M[r][c]==0:
				piecesTurned= LocateTurnedPieces(r, c, player, M)
				if len(piecesTurned)!=0:
					moves.append((r,c))
	return np.array(moves, dtype=tuple)

cdef LocateTurnedPieces(int r, int c, player, DTYPE_t[:,:] M): # The pieces turned over are of -player's color. A zero in a
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

	return np.array(totalFlipped, dtype=DTYPE)

