import random
playingBoard = [[" ", " ", " "],
                [" ", " "," "],
                [" ", " ", " "]]


keyBoard = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]]

currentPlayer = 0 # 0 = human, 1 = computer
global humansPiece 
humansPiece = "X"
global computersPiece 
computersPiece = "O"

possibleLines = [ #list of all possible lines
                    [1,2,3], 
                    [4,5,6], 
                    [7,8,9],
                    [1,4,7],
                    [2,5,8],
                    [3,6,9],
                    [1,5,9],
                    [3,5,7]
                ]

def printBoard(board):
    print("-------------")
    for i in range(3): #i is the row
        print(f'| {board[i][0]} | {board[i][1]} | {board[i][2]} |')
        print("-------------")

def getCurrentPiece() -> str:
    global currentPlayer
    if currentPlayer == 0:
        return humansPiece
    else:
        return computersPiece

    
def findLocation(key: int) -> list: #returns the coordinates of the square labelled with the given key
    row = 0
    if key <= 3:
        row = 0
    elif key <= 6:
        row = 1
    else:
        row = 2
    column = 0
    for i in range(3):
        if keyBoard[row][i] == key:
            column = i
    return [row, column]

def getSquareContents(key: int) -> str:
    coords = findLocation(key)
    return playingBoard[coords[0]][coords[1]]

def setSquareContents(key: int, piece: str) -> None:
    coords = findLocation(key)
    playingBoard[coords[0]][coords[1]] = piece

def setPieces():
    valid = False
    global humansPiece 
    global computersPiece 
    global currentPlayer
    while valid == False:
        if currentPlayer == 0:
            piece = input("Enter which piece you would like to play as: [Enter O or X]")
            if piece == "X":
                humansPiece = "X"
                computersPiece = "O"
                valid = True
            else:
                humansPiece = "O"
                computersPiece = "X"
                valid = True
        else:
            if random.randint(0,1) == 0:
                humansPiece = "X"
                computersPiece = "O"
            else:
                humansPiece = "O"
                computersPiece = "X"

def makeMove():
    valid = False
    while valid == False:
        choice = input("Enter where you would like to put a piece: ")
        if choice.isdigit():
            choice = int(choice)
            if choice < 0 or choice > 9:
                print("Invalid choice! Out of range")
            else:
                if getSquareContents(choice) != " ":
                    print("This square is not empty!")
                else:
                    valid = True
        else:
            if choice == "k":
                printBoard(keyBoard)
            elif choice == "x":
                print("Goodbye!")
                return
            else:
                print("That's not an option!")
    setSquareContents(choice, getCurrentPiece())

def checkForWinner(piece: str) -> bool:
    for line in possibleLines:
        count = 0
        for i in line:
            if getSquareContents(i) == piece:
                count += 1
        if count == 3:
            return True
    return False

def checkForLine(line: list, piece: str, opposingPiece: str) -> bool:
    count = 0
    for i in line:
        if getSquareContents(i) == piece:
            count += 1
        elif getSquareContents(i) == opposingPiece:
            return False
    if count == 2:
        return True
    return False

def completeLine(line: list) -> bool: #works out if a line can be completed to win the game
    return checkForLine(line, computersPiece, humansPiece)

def blockLine(line: list) -> bool: #works out if the oppsoing player is about to complete a line
    return checkForLine(line, humansPiece, humansPiece)

def makeAPair(line: list) -> bool: 
    count = 0
    for i in line:
        if getSquareContents(i) == computersPiece:
            count += 1
        elif getSquareContents(i) == humansPiece: #if potential line contains one of the humans pieces, a winning line can't be made here
            return False
    return count == 1 #return true if a computers piece is already in the potential line

def findPossibleMoves() -> list:
    possibleMoves = []
    for line in possibleLines:
        count = 0
        if completeLine(line):
            possibleMoves.append(3) #completing a line has highest priority
        elif blockLine(line):
            possibleMoves.append(2) 
        elif makeAPair(line):
            possibleMoves.append(1)
        else:
            possibleMoves.append(0)
    return possibleMoves

def computerMove():
    possibleMoves = findPossibleMoves()
    highestPriority = 0
    for i in possibleMoves:
        if highestPriority < i:
            highestPriority = i #finds highest priority in list
    for i in range(8):
        if possibleMoves[i] == highestPriority:
            line = possibleLines[i]
            nextMove = 0
            for i in range(3):
                if getSquareContents(line[i]) == " ":
                    setSquareContents(line[i], computersPiece)
                    return
    
    randomLocation = 0 #if a good move can't be found, randomly place the piece on a free square
    while getSquareContents(randomLocation) != " ":
        randomLocation = random.randint(1, 9)
    setSquareContents(randomLocation, computersPiece)
            
    
def playGame():
    setPieces()
    printBoard(playingBoard)
    gameWon = False
    totalPieces = 0
    global humansPiece 
    global computersPiece 
    global currentPlayer
    while gameWon == False and totalPieces < 9:
        if currentPlayer == 0:
            makeMove()
            totalPieces += 1
            print("Your move:")
            printBoard(playingBoard)
            if checkForWinner(humansPiece):
                print("Congratulations! You won!")
                gameWon = True
            currentPlayer = 1
        else:
            computerMove()
            totalPieces += 1
            print("Computer's move:")
            printBoard(playingBoard)
            if checkForWinner(computersPiece):
                print("You lose!")
                gameWon = True
            currentPlayer = 0
    if totalPieces == 9:
        print("The game is a draw!")


playGame()
