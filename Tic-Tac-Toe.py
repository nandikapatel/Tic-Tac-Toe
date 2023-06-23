app.rows = 3
app.cols = 3
app.board = makeList(app.rows, app.cols)
board = Group()

def initializeGame():
    # Create the board and initialize game properties.
    cellSize = 400 / 3
    for row in range(app.rows):
        for col in range(app.cols):

            # Calculate x, y for each row, col and add a rectangle to
            # the board group.
            x = col * cellSize 
            y = row * cellSize
            board.add(
                Rect(x, y, cellSize, cellSize, fill = 'skyBlue', borderWidth = 5, border = 'lightCyan')
                )

            # Calculate the center of each cell and add a label there.
            # Also assign the label into app.board and add it to the board Group.
            centerX = x + (cellSize/2)
            centerY = y + 67
            centerLabel = Label('', centerX, centerY, bold = True, size = 90)
            app.board[row][col] = centerLabel


    # The current player: 'O' or 'X'.
    app.player = 'O'

    # The game status.
    app.isGamePlaying = False

initializeGame()

# Draws the label indicating nextPlayer.
Rect(120, 5, 160, 30, fill='hotPink', opacity=50)
Label('Next Player: ', 190, 20, fill='white', size=15, bold=True)
nextPlayer = Label(app.player, 250, 20, fill='white', size=15, bold=True)

# Defines gameOver and newGame screens.
newGameScreen = Group(
    Rect(0, 100, 400, 200, fill='aliceBlue', opacity=70),
    Label('Welcome to Tic-Tac-Toe!', 200, 190, fill='darkOrange', size=30,
          bold=True),
    Label('press space to start a new game', 200, 220, fill='darkOrange',
          size=15, bold=True)
    )

# Draws and setss gameOverScreen.
gameOverScreen = Group(
    Rect(0, 0, 400, 400, fill='aliceBlue', opacity=70),
    Label('press "r" to restart', 200, 250, fill='darkOrange', size=20, bold=True)
    )

winningMessage = Label('', 200, 200, fill='darkOrange', size=50, bold=True)
gameOverScreen.add(winningMessage)
gameOverScreen.visible = False


def isValidMove(row, col):

    # Check if the grid for the next step is empty.
    # if app.board[row][col].value != None:
    if (app.board[row][col].value == ''):
        return True
    else:
        return False


def makeMove(row, col):

    # Set the value at row, col to app.player and set the color depending on
    # if the player is 'X' or 'O'.
    app.board[row][col].value = app.player
    if app.player == 'O':
        app.board[row][col].fill = 'steelBlue'
    else:
        app.board[row][col].fill = 'white'


def findCell(mouseX, mouseY):
    size = 400 / 3
    for row in range(app.rows):
        for col in range(app.cols):
            x = col * size
            y = row * size

            # If the mouseX, mouseY is between the boundaries of a cell,
            # returns the coordinates of that cell.
            if ((x <= mouseX) and (mouseX <= x + size) and
                (y <= mouseY) and (mouseY <= y + size)):
                return [ row, col ]

def getColumn(board, col):
    # Return a list of all values in the column.
    colList = [ ]
    ### (HINT: Append the element at col for each row in the board.)
    ### Place Your Code Here ###
    for row in board:
        colList.append(row[col])
    return colList

def checkWin(colRowOrDiag):
    # The input is either a row, column, or diagonal list that a win could
    # be on. Return a boolean that states whether or not there is a winning
    # condition given the input.
    count = 0
    ### (HINT: There is a winning condition if every cell in the input has
    #          the same label as the player!)
    ### Place Your Code Here ###
    for cell in colRowOrDiag:
        if cell.value == app.player:
            count += 1

    if count == 3:
        return True 
    else:
        return False
   
    # for cell in colRowOrDiag:
    #     if cell == app.player:
    #         count += 1
    #         print('app.player: ' + app.player + ', cell: '+ cell + ', count: ' + str(count))
    #         print(colRowOrDiag)

    # if count == 3:
    #     return True
    # else:
    #     return False

def checkTie():
    # If there are no empty spaces left, there's a tie.
    for row in range(app.rows):
        for col in range(app.cols):
            if (app.board[row][col].value == ''):
                return False
    return True

def checkGameWin():
    # Checks if there is a winning row.
    for row in app.board:
        if (checkWin(row) == True):
            return True

    # Checks if there is a winning column.
    for col in range(3):
        colList = getColumn(app.board, col)
        if (checkWin(colList) == True):
            return True

    # Gets the top-left to bottom-right diagonal.
    diagonalLeftToRight = [ app.board[0][0], app.board[1][1], app.board[2][2] ]

    # Gets the top-right to bottom-left diagonal.
    diagonalRightToLeft = [ app.board[0][2], app.board[1][1], app.board[2][0] ]

    # Checks if there is a winning diagonal.
    if (checkWin(diagonalLeftToRight) == True):
        return True
    if (checkWin(diagonalRightToLeft) == True):
        return True

    return False

def gameOver(winOrTie):
    if (winOrTie == 'Win'):
        app.isGameOn = False
        gameOverScreen.visible = True
        winningMessage.value = 'Winner: ' + app.player + ' !'
    elif (winOrTie == 'Tie'):
        app.isGameOn = False
        gameOverScreen.visible = True
        winningMessage.value = 'Tie!'

def onMousePress(mouseX, mouseY):
    if (app.isGamePlaying == True):
        position = findCell(mouseX, mouseY)
        row = position[0]
        col = position[1]
        if (isValidMove(row, col) == True):
            makeMove(row, col)

            # If the game ends, update gameOver screen.
            if (checkGameWin() == True):
                gameOver('Win')
            elif (checkTie() == True):
                gameOver('Tie')

            # Changes the player turn.
            if (app.player == 'O'):
                app.player = 'X'
            else:
                app.player = 'O'

            # Updates the nextPlayer value.
            nextPlayer.value = app.player

def onKeyPress(key):

    # Start a new game or restart the game.
    # When space is pressed and the game is not already playing,
    # make the newGameScreen invisible and set isGamePlaying.
    if ('space' in key) and (app.isGamePlaying == False):
        newGameScreen.visible = False
        app.isGamePlaying = True

    # When r is pressed, restarts the game.
    if (key == 'r'):
        gameOverScreen.visible = False
        board.clear()
        initializeGame()
        nextPlayer.value = app.player
        app.isGamePlaying = True
