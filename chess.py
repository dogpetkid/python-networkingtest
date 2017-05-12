##Chess written by Dogpetkid

##Imports
import os
from Choose import *
try: import winsound
except: pass
try: ##Import the multiplayer additions
    from clienttest import *
    from servertest import *
    multi = True
except:
    multi = False

##Mess alert
print("If you see this... you might have a box that just pops on your screen later in the game (AND IT CAN GET ANNOYING).")
os.system('cls' if os.name == 'nt' else 'clear')

##Commenting system:

##Single Pound (#) = Comment out code
##Single Pound-Dollar (#$) = Go back and fix
##Double Pounds (##) = Comment
##Double Pound-At (##@) = Chess/Code Comment
##Triple Pound (###) = Code Probe/Tracer
##(Not all cases follow this system but most do for convenience)

##Dictionary:

##@File and Rank: equivilent of x and y but File is a through h and Rank is 1 through 8
##@A DSCheck (Diagonal-Stright Check): checking for bishops and queens on diagonals, rooks and queens on strights, knights on Ls, pawns on near diagonal, and kings on king-array (this is used for the king)

##To do:

##Add Edgecase moves (Castling + En Passant)
##Add graphics board
##Add Checkmate
##Add stalemate


class RankFileError(Exception):
    ##Error some of the folloring code using ranks and files
    message = "NotationConversion was given an inncorrect value of rankfile."

colors = ["Black","White"]
##Asks for the function under this one to run or not
notation = ""
printfile = ""
printrank = ""
flip = ""
def asknotation():
    ##At the start of the program, it asks way co-ordinates will be represented and which way the board should be looked at
    global notation
    global printfile
    global printrank
    global flip
    notation = choose2("Use Chess Notation (1) or Array Coords (0).","1","0",1)
    if notation == "1":
        notation = True ##Uses Chess Notation
    else:
        notation = False ##Uses Array co-ordinates
    if notation: ##Describes the way to say x in y but in chess form
        printfile = "File" 
        printrank = "Rank"
    else:
        printfile = "x"
        printrank = "y"
    setflip = choose2("Flip the board on black's turn?","y","n",1)
    if setflip == "n": ##Sets up the range function parameters here so that you get 7,6,5,4...0 for counting down the y and then 0,1,2,3...7 for the x (the first element is the array of turples for black y and then black x and the other element is turples for white y and white x)
        flip = [[(7,-1,-1),(0,8,1)],[(7,-1,-1),(0,8,1)]]
    elif setflip == "y": ##Only difference is the black is fliped so the board is 'fliped' as if they were looking at it (so 0,1,2,3...7 on y and 7,6,5,4...0 on x)
        flip = [[(0,8,1),(7,-1,-1)],[(7,-1,-1),(0,8,1)]]
    os.system('cls' if os.name == 'nt' else 'clear')

##Conversion of notation to arraycode
##rankfile is either "rank" or "file"
def notationcon(val,rankfile):
    global notation
    if notation: ##If chess notation...
        try:
            if rankfile == "file": ##Files are letters that need to be turned into numbers a = 0, b = 1... h = 7
                val = val.lower()
                val = ord(val)-97
            elif rankfile == "rank": ##Ranks are numbers that just need to be shifted down one so they are array element numbers 1 = 0, 2 = 1... 8 = 7
                val = int(val)-1
            else: ##If there is no conversion specified, crash the program forcefully
                raise RankFileError(RankFileError.message)
            return val
        except:
            raise RankFileError("Something was input wrong...") ##If an incorrect value somehow causes an issue
    else: ##Else no conversion...
        return int(val)

##Simple way to get array format for x or y based on file or rank
def getxy(rankfile):
    ##Takes an input in order to get an x or y value
    while True:
        try:
            val = input(rankfile + ": ") ##Asks and...
            val = notationcon(val,rankfile.lower()) ##Converts
        except ValueError:
            print("Numbers please.")
            continue
        except RankFileError:
            print("Something went wrong...")
            continue
        if val in range(8): ##Makes the value be on the 8 by 8 board
            break
        else:
            print("Value must be on board.")
    return val


class piece():
    def __init__(self,rank,file,color):
        self.x = rank
        self.y = file
        ##Color is described as
        ##White = 1
        ##Black = 0
        self.color = color
        self.letter = (type(self).__name__)[:1] ##Sets the letter to print the piece as the first letter...
        if type(self).__name__ == "knight": ##unless it is a knight, knights are n's
            self.letter = "n"
        if self.color == 1: ##If the piece is white it has a capital letter
            self.letter = self.letter.capitalize()
        if type(self).__name__ == "king": ##King goes on the kinglist
            kings.append(self)
            
    def me(self):
        return[self.x,self.y,self.color,type(self).__name__]
    def coords(self):
        return[self.x,self.y]
    def piece(self):
        return(type(self).__name__)
    
    ##Upgrade should not be stated unless the promotion of the piece is known
    def moveme(self,coords,upgrade=True):
        ##Movement is the deletion of the old object and cloning it into it's new location (like teleportation but in an array)
        board.square[self.x][self.y] = ""
        self.x = coords[0]
        self.y = coords[1]
        board.square[self.x][self.y] = self
        try:
            self.moved = True
            ##Pawn promotion:
            ##If a pawn gets to the last rank of the rank
            if self.piece() == "pawn" and self.y == 7 and upgrade == True: ##The upgrade=True in the defenition is so a forceful promotion (for playing multiplayer) is possible
                upgrade = choosen("Promote your pawn, choose a piece:",["rook","bishop","knight","queen"],1)
            if upgrade == "rook":
                action = rook
            elif upgrade == "bishop":
                action = bishop
            elif upgrade == "knight":
                action = knight
            elif upgrade == "queen":
                action = queen
            if self.piece() == "pawn" and self.y == 7:
                ##Changes the pawn whith it's new form
                board.square[self.x][self.y] = action(self.x,self.y,self.color)
                board.square[self.x][self.y].moved = True
                return upgrade ##Allows for the program to know what you promoted the piece into
        except:
            pass
        return ""
        


class pawn(piece):
    moved = False
    
    def moves(self):
        moves = []
        x = self.x
        y = self.y
        
        ##Based on color changes the direction of travel
        if self.color == 1:
            ##Checks the square ahead
            try:
                front = board.square[x][y+1]
            except:
                front = "off"
            if front == "":
                moves.append([x,y+1])
                ##Checks the square 2 ahead
                try:
                    doublefront = board.square[x][y+2]
                except:
                    doublefront = "off"
                ##If the pawn hasn't been moved before, then it can move 2 squares
                if doublefront == "" and not(self.moved):
                    moves.append([x,y+2])
            
            ##Checks diagonal attacks by looking 1 to the left and right of the direction it looks
            for i in [1,-1]:
                try:
                    square = board.square[x+i][y+1]
                    if square.color != self.color:
                        moves.append([x+i,y+1])
                except:
                    square = -1
        
        else:
            ##Checks the square ahead
            try:
                front = board.square[x][y-1]
            except:
                front = "off"
            if front == "":
                moves.append([x,y-1])
                ##Checks the square 2 ahead
                try:
                    doublefront = board.square[x][y-2]
                except:
                    doublefront = "off"
                ##If the pawn hasn't been moved before, then it can move 2 squares
                if doublefront == "" and not(self.moved):
                    moves.append([x,y-2])
            
            ##Checks diagonal attacks by looking 1 to the left and right of the direction it looks
            for i in [1,-1]:
                try:
                    square = board.square[x+i][y-1]
                    if square.color != self.color:
                        moves.append([x+i,y-1])
                except:
                    square = -1
        
        #$Add En Passant here
        
        return moves

class rook(piece):
    moved = False
    
    def moves(self):
        moves = []
        x = self.x
        y = self.y
        
        ##The rook checks the x in both directions and then the y
        ##It looks in a direction moving the x to the edge of the board but keeps the same y
        ##Then it swaps and does that for the y and retains the x
        
        ##Checks to the right
        for i in range(x+1,8): ##Looks to the edge
            square = board.square[i][y]
            ##Checks if the square is empty or a piece of the color (and it can move there)
            if square == "":
                moves.append([i,y])
            else:
                if square.color != self.color:
                    moves.append([i,y])
                break
        
        ##Checks the left
        for i in range(x-1,-1,-1):
            square = board.square[i][y]
            if square == "":
                moves.append([i,y])
            else:
                if square.color != self.color:
                    moves.append([i,y])
                break
        
        ##Checks the top
        for i in range(y+1,8):
            square = board.square[x][i]
            if square == "":
                moves.append([x,i])
            else:
                if square.color != self.color:
                    moves.append([x,i])
                break
        
        ##Checks the bottom
        for i in range(y-1,-1,-1):
            square = board.square[x][i]
            if square == "":
                moves.append([x,i])
            else:
                if square.color != self.color:
                    moves.append([x,i])
                break
        return moves

class knight(piece):
    def moves(self):
        moves = []
        x = self.x
        y = self.y
        
        ##The knight checks the by 2 up then 2 down with its left and right neighbor and repeast a similar process for 2 on the x and 1 on the y
        for yn in [2,-2]: ##Checks 2 in the y
            for xn in [-1,1]: ##and one in the x
                ##Check if the square is on the board
                if x+xn in range(8) and y+yn in range(8):
                    square = board.square[x+xn][y+yn]
                    ##The reason to check if the square is empty is not to cause a str.color error
                    if square == "":
                        moves.append([x+xn,y+yn])
                    elif square.color != self.color:
                        moves.append([x+xn,y+yn])
        
        ##Repeats the above but with different directions
        for xn in [2,-2]:
            for yn in [-1,1]:
                if x+xn in range(8) and y+yn in range(8):
                    square = board.square[x+xn][y+yn]
                    if square == "":
                        moves.append([x+xn,y+yn])
                    elif square.color != self.color:
                        moves.append([x+xn,y+yn])
        return moves

class bishop(piece):
    def moves(self):
        moves = []
        x = self.x
        y = self.y
        
        ##Bishop goes checks the four directions and moves a 'cursor' onto that spot and checks if it is empty or a piece of the opposite color
        ##It continues till it hits a piece or goes off the board
        for d in [[1,1],[-1,1],[-1,-1],[1,-1]]:
            posx = x
            posy = y
            while True:
                ##Looks at 1 square in the direction that a bishop moves
                posx+=d[0]
                posy+=d[1]
                square = -1
                ##Check if the square is on the board
                if posx in range(8) and posy in range(8):
                    square = board.square[posx][posy]
                else:
                    break
                ##Check if the square is empty
                if square == "":
                    moves.append([posx,posy])
                else:
                    ##Check if the piece is not my color
                    if square.color != self.color:
                        moves.append([posx,posy])
                    break
        return moves

class queen(piece):
    def moves(self):
        ##Queen is a copy of the rook and bishop so it uses the .moves from both of their classes
        moves = rook.moves(self)
        moves += bishop.moves(self)
        return moves

kings = []
class king(piece):
    moved = False
    ##@Before a piece moves check its location to see if it can attack the king of the opposite color, if yes, set his check to TRUE
    
    ##@Three ways out of check: Attack, Block, Move
    ##@Do a DSCheck to find the attacker and record his position (say pieces can attack there if there is only 1)
    ##@Do a moves check of the attacker and a moves check of the same piece from the position of the king and those spaces can be blocks (if there is only 1 and the single attacker is not a knight or pawn)
    ##@Check the squares a king can go to and DSCheck them
    def dscheck(self): ##A DSCheck consists of all the piece moves from the kings position to check if they are there
        attacker = []
        x = self.x
        y = self.y
        
        ##The dscheck uses the moves of each piece but alters the way it is used:
        ##it uses is the same except it checks if a square is filled with a specific piece (depending on what piece moves that way)
        ##and it stops when it sees it's own piece (unless it is a king because he can't block for himself)
        
        ##Checks straights
        ##Checks to the right
        for i in range(x+1,8):
            square = board.square[i][y]
            if square != "":
                if square.color != self.color and (square.piece() == "rook" or square.piece() == "queen"):
                    attacker.append([i,y])
                elif not(square.color == self.color and square.piece() == "king"):
                    break
        
        ##Checks the left
        for i in range(x-1,-1,-1):
            square = board.square[i][y]
            if square != "":
                if square.color != self.color and (square.piece() == "rook" or square.piece() == "queen"):
                    attacker.append([i,y])
                elif not(square.color == self.color and square.piece() == "king"):
                    break
        
        ##Checks the top
        for i in range(y+1,8):
            square = board.square[x][i]
            if square != "":
                if square.color != self.color and (square.piece() == "rook" or square.piece() == "queen"):
                    attacker.append([x,i])
                elif not(square.color == self.color and square.piece() == "king"):
                    break
        
        ##Checks the bottom
        for i in range(y-1,-1,-1):
            square = board.square[x][i]
            if square != "":
                if square.color != self.color and (square.piece() == "rook" or square.piece() == "queen"):
                    attacker.append([x,i])
                elif not(square.color == self.color and square.piece() == "king"):
                    break
        
        
        ##Checks diagonals
        for d in [[1,1],[-1,1],[-1,-1],[1,-1]]:
            posx = x
            posy = y
            while True:
                ##Looks at 1 square
                posx+=d[0]
                posy+=d[1]
                square = -1
                ##Check if the square is on the board
                if posx in range(8) and posy in range(8):
                    square = board.square[posx][posy]
                else:
                    break
                ##Check if the square is empty
                if square != "":
                    if square.color != self.color and (square.piece() == "bishop" or square.piece() == "queen"):
                        attacker.append([posx,posy])
                    elif not(square.color == self.color and square.piece() == "king"):
                        break
        
        
        ##Checks L's
        for yn in [2,-2]:
            for xn in [-1,1]:
                ##Check if the square is on the board
                if x+xn in range(8) and y+yn in range(8):
                    square = board.square[x+xn][y+yn]
                    ##The reason to check if the square is empty is not to cause a str.color error
                    if square != "":
                        if square.color != self.color and square.piece() == "knight":
                            attacker.append([x+xn,y+yn])
        
        ##Repeats the above but with different directions
        for xn in [2,-2]:
            for yn in [-1,1]:
                if x+xn in range(8) and y+yn in range(8):
                    square = board.square[x+xn][y+yn]
                    if square != "":
                        if square.color != self.color and square.piece() == "knight":
                            attacker.append([x+xn,y+yn])
        
        
        ##Check near diagonals
        for xn in [-1,1]:
            if self.color == 1:
                coords = [x+xn,y+1]
            else:
                coords = [x+xn,y-1]
            if coords[0] in range(8) and coords[1] in range(8):
                square = board.square[coords[0]][coords[1]]
            else:
                square = ""
            if square != "":
                if square.color != self.color and square.piece() == "pawn":
                    attacker.append(square.coords())
        
        
        ##Checks donuts (spaces around a king)
        karray = []
        for xi in range(-1,2):
            for yi in range(-1,2):
                ##Checks if it is on the board and not the current space
                if x+xi in range(8) and y+yi in range(8) and (xi != 0 or yi != 0):
                    karray.append([x+xi,y+yi])
        for val in karray:
            square = board.square[val[0]][val[1]]
            if square != "":
                if square.color != self.color and square.piece() == "king":
                    attacker.append([val[0],val[1]])
        
        return attacker
    
    def moves(self):
        moves = []
        pmoves = [] ##This is so the actual possible moves
        x = self.x
        y = self.y
        
        ##Sets up donut (the array of sqaures around the king)
        karray = []
        for xi in range(-1,2):
            for yi in range(-1,2):
                ##Sets the *possible* spaces to all the around squares
                if x+xi in range(8) and y+yi in range(8) and (xi != 0 or yi != 0):
                    karray.append([x+xi,y+yi])
        ##This reduces the amount of dschecks the king will have to take by removing square that can't be occupyed to begin with
        for val in karray:
            square = board.square[val[0]][val[1]]
            if square == "":
                pmoves.append([val[0],val[1]])
            else:
                if square.color != self.color:
                    pmoves.append([val[0],val[1]])
        
        for m in pmoves:
            ##Mocks the king moving to spaces and checking for check
            px = m[0]
            py = m[1]
            self.x = px
            self.y = py
            dsatt = self.dscheck()
            if len(dsatt) == 0:
                moves.append(m)
        
        #$Add Castling here
        
        self.x = x
        self.y = y
        return moves
    
    def blocking(self,other):
        ##@Better block explanation:
        ##@Since a piece can be placed between the attacker, this is a way out of check
        ##@Because of the nature of pawns and knights (they can't get blocked), they are excuded from this process below
        if other.piece == "pawn" or other.piece() == "knight":
            return []
        ##@The remaining pieces (minus the king because he can't cause check) have to have their moves checked from their position and the position of the king being attacked
        fromhome = other.moves()
        homex = other.x
        homey = other.y
        other.x = self.x
        other.y = self.y
        fromking = other.moves()
        other.x = homex
        other.y = homey
        ##@The overlaping squares should narrow this close to what we need
        possible = []
        for test in fromhome:
            if test in fromking:
                possible.append(test)
        ##@Now a list of square they can attack should give us the squares that can be blocked from...
        ##@ But because there can be overlaps that are not between the king and attacker, we have to check a rectangle from the king to the attacker, giving us the actuall squares that block (minus the corners of that rectangle)
        boxx = range(min([self.x,other.x]),max([self.x,other.x])+1)
        boxy = range(min([self.y,other.y]),max([self.y,other.y])+1)
        fourcorners = [[min(boxx),max(boxy)],[max(boxx),min(boxy)],[min(boxx),min(boxy)],[max(boxx),min(boxy)]]
        realpossible = []
        for test in possible:
            if test[0] in boxx and test[1] in boxy and not([test[0],test[1]] in fourcorners):
                realpossible.append(test)
        ##@After removing all false cases, these should be the actuall squares to block from
        return realpossible


class board:
    
    ##Sets ups the board spaces
    square = []
    for i in range(8):
        square.append(["","","","","","","",""])
        
    # # # # # # # # # #
    
    ##White pieces
    for x in range(8):
        square[x][1] = pawn(x,1,1)
    for x in [0,7]:
        square[x][0] = rook(x,0,1)
    for x in [1,6]:
        square[x][0] = knight(x,0,1)
    for x in [2,5]:
        square[x][0] = bishop(x,0,1)
    square[3][0] = queen(3,0,1)
    square[4][0] = king(4,0,1)
    
    ##Black pieces
    for x in range(8):
        square[x][6] = pawn(x,6,0)
    for x in [0,7]:
        square[x][7] = rook(x,7,0)
    for x in [1,6]:
        square[x][7] = knight(x,7,0)
    for x in [2,5]:
        square[x][7] = bishop(x,7,0)
    square[3][7] = queen(3,7,0)
    square[4][7] = king(4,7,0)
    '''
    square[3][2] = king(3,2,1)
    square[4][3] = queen(4,3,0)
    square[5][2] = knight(5,2,0)
    ''''''
    square[4][1] = queen(4,1,1)
    square[2][2] = king(2,2,1)
    square[0][0] = king(0,0,0)
    '''
    
    # # # # # # # # # #
    
    def asciiboard(color=1,moves=[]): ##Prints the board
        ##Configures the top and header of the board
        ##Based apon the choice of the notation and the fliping the board changes the header, sides, and footer of the board
        asciiboard = []
        if notation: ##Arranges the letters on the top of the board
            letterrow = ""
            for x in range(flip[color][1][0],flip[color][1][1],flip[color][1][2]):
                letterrow+=chr(x+97)+"-"
            asciiboard.append("+--"+letterrow+"-+")
        else: ##Arranges the numbers on the top of the board
            numrow = ""
            for x in range(flip[color][1][0],flip[color][1][1],flip[color][1][2]):
                numrow+=str(x) + "-"
            asciiboard.append("+--"+numrow+"-+")
        asciiboard.append("|  + + + + + + + +  |")
        
        ##The point in the *flip* variable is to literally flip the board the other way for the black's turn (if selected in the start of the program)
        
        ##Configures the body and sides of the board
        for y in range(flip[color][0][0],flip[color][0][1],flip[color][0][2]):
            row = ""
            for x in range(flip[color][1][0],flip[color][1][1],flip[color][1][2]):
                ##Puts the moves on the board
                if [x,y] in moves and board.square[x][y] == "":
                    row += "o "
                elif [x,y] in moves:
                    row += "X "
                ##Puts the letters of pieces on the board (and blanks)
                else:
                    try:
                        row += board.square[x][y].letter + " " 
                    except:
                        row += "- "
            ##Sets the number for the side of the board based on chess notation or array co-ordinates
            if notation:
                side = y+1
            else:
                side = y
            asciiboard.append(str(side)+"+ "+row+"+"+str(side))
            ##Puts a space between rows of the board
            if y != (flip[color][0][1]-flip[color][0][2]):
                asciiboard.append("|                   |")
        
        ##Configues the bottom and footer of the board
        asciiboard.append("|  + + + + + + + +  |")
        if notation:
            asciiboard.append("+--"+letterrow+"-+")
        else:
            asciiboard.append("+--"+numrow+"-+")
        for asc in asciiboard:
            print(asc)
    
    def turn(color):
        global multi
        ##Function to remove moves that don't get the king out of check
        def widdle(checkpossible,square,check,possible):
            realpossible = []
            if len(checkpossible) > 0 and not(square.piece() == "king") and check:
                for test in possible: ##Does check conditional
                    if test in checkpossible:
                        realpossible.append(test)
            return realpossible
        
        ##@Go to king class to see the specifications for the king check cases
        attackers = []
        colorking = []
        checkpossible = []
        check = False
        for king in kings: ##Goes through to see if there is check
            if king.color == color: ##Checks if this is playing team's king
                ds = king.dscheck()
                if len(ds) > 0: ##Since the king is being attacked, he is added to kings list of my color and being attacked
                    colorking.append(king)
                attackers += ds ##Then record the attacker
        
        if len(attackers) > 0: ##If the king is in check...
            check = True
            if len(attackers) == 1 and len(colorking) == 1: ##make the squares pieces other than the king to limited by checking how to block/kill the attacker (you can only block for 1 piece attacking)
                attsquare = board.square[attackers[0][0]][attackers[0][1]] ##(Records attacker)
                checkpossible = attackers + colorking[0].blocking(attsquare) ##Check to see how to block against the attacker or kill him
        try:
            if len(checkpossible+colorking[0].moves()) == 0: ##If the king can not legally move and other pieces can't move then the game *MAY* be over
                possibleendgame = []
                for x in range(8):
                    for y in range(8):
                        square = board.square[x][y]
                        if square == "":
                            pass
                        elif square.color == color:
                            possibleendgame+=square.moves()
                
                #$Finish the ending game code here
                '''realendgame = []
                if len(checkpossible) > 0 and not(square.piece() == "king") and check:
                    for test in possible: ##Does check conditional
                        if test in possibleendgame:
                            realendgame.append(test)
                '''
                
                if len(possibleendgame) == 0:#$Fix so that endgame works
                    if check:
                        return ["Checkmate"]
                    else:
                        return ["Stalemate"]
        except:
            pass
        
        global printfile
        global printrank
        
        if color == 1:
            input("White's Turn...")
        else:
            input("Black's Turn...")
        while True: ##Loops till turn is taken
            if check:
                print("!       CHECK       !")
            board.asciiboard(color)
            ##Piece selection
            while True: ##Loops till piece is selected
                x = getxy(printfile)
                y = getxy(printrank)
                square = board.square[x][y]
                if square == "":
                    input("Pick a piece of your color. (Hit enter)")
                    continue
                elif square.color == color:
                    break
                input("Pick a piece of your color. (Hit enter)")
            
            ##Movement selection (or back to piece selection)
            possible = square.moves()
            ##Makes sure you have to get yourself out of check by limiting your moves in check
            realpossible = []
            if len(checkpossible) > 0 and not(square.piece() == "king") and check:
                for test in possible: ##Does check conditional
                    if test in checkpossible:
                        realpossible.append(test)
            elif square.piece() == "king" or not(check):
                realpossible = possible
            
            if realpossible == []:
                input((square.piece()).capitalize() + " has no valid moves. (Hit enter)")
                continue
            board.asciiboard(color,realpossible)
            xm = getxy(printfile)
            ym = getxy(printrank)
            if not([xm,ym] in realpossible):
                input("That is not a possible move... sending you back to piece selection. (Hit enter)")
                continue
            ##Piece movement
            promote = square.moveme([xm,ym])
            input("(Hit enter)")
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        return ["",x,y,xm,ym,promote]



##Below is some test code for checking the board
def test():
    global printfile
    global printrank
    input(board.square)
    print()
    for i in range(8):
        input(board.square[i])
    print()
        
    while True: ##The point of all the try-except cases below is to have crashes only be real errors in code and not mishaps of the user
        if input("To break type 'b'") == "b":
            break
        board.asciiboard(color)
        x = getxy(printfile)
        y = getxy(printrank)
        try:
            print(board.square[x][y])
            print(board.square[x][y].color)
            print(board.square[x][y].coords())
            print(board.square[x][y].moves())
        except Exception as e:
            print("Error: " + str(type(e)) + " --> " + str(e))
            continue
        input()
        os.system('cls' if os.name == 'nt' else 'clear')
    board.turn(1)
    board.asciiboard(color)
    input("Don't press")

##Below is the game turn cycle
def gamecycleHOTSEAT():
    print("Game starts with white")
    while True:
        ##The 'end' variable is a message for the end of the game
        #$but the game does not end yet...
        end = board.turn(1)[0]##Ignores muliplayer responces
        if end != "":
            input(end)
            if end == "Checkmate":
                input("Black wins")
                break
        end = board.turn(0)[0]##Ignores multiplayer responces
        if end != "":
            input(end)
            if end == "Checkmate":
                input("White wins")
                break
    input("(To leave press enter 1 last time.)")

def gamecycleSIDEHOST():
    global chessconnection
    global colors
    sidecolor = choose2("Color? White(1) or Black(0)","1","0",1)
    speak(chessconnection,sidecolor)
    sidecolor = int(sidecolor)
    oppcolor = (int(sidecolor)+1)%2
    try:
        turncolor = 1
        while True: ##Turn distributer
            if turncolor == sidecolor:
                input("Your turn: ")
                try: winsound.PlaySound(None,0)
                except: pass
                moves = board.turn(sidecolor)
                if moves[0] != "":
                    input(end)
                    if end == "Checkmate":
                        input(colors[oppcolor]+" wins.")
                        break
                packmoves = arraypackage(moves[1:])
                speak(chessconnection,packmoves)
            else:
                print("Opponent's turn...")
                board.asciiboard(sidecolor)
                packoppmoves = listen(chessconnection)
                oppmoves = arrayunpackage(packoppmoves)
                for i in range(4):
                    oppmoves[i] = int(oppmoves[i])
                square = board.square[oppmoves[0]][oppmoves[1]]
                square.moveme([oppmoves[2],oppmoves[3]],oppmoves[4])
                os.system('cls' if os.name == 'nt' else 'clear')
                try: winsound.PlaySound("SystemExclamation",winsound.SND_ASYNC | winsound.SND_LOOP)
                except: pass
            ##Rotate turn
            turncolor = (turncolor+1)%2
        input("Game over")
    except LostComs:
        chessconnection.close()
        input("Lost communication... continuing to single sided play.")
        gamecycleUNISIDE(turncolor)

def gamecycleSIDECLIENT():
    global chessconnection
    global colors
    print("Waiting for HOST to pick their color.")
    oppcolor = listen(chessconnection)
    sidecolor = (int(oppcolor)+1)%2 ##I know the other side's color so I can add 1 and mod 2 (white(1)+1>>2>>0, black(0)+1>>1%2>>1)
    try:
        turncolor = 1
        while True: ##Turn distributer
            if turncolor == sidecolor:
                input("Your turn: ")
                try: winsound.PlaySound(None,0)
                except: pass
                moves = board.turn(sidecolor)
                if moves[0] != "":
                    input(end)
                    if end == "Checkmate":
                        input(colors[oppcolor]+" wins.")
                        break
                packmoves = arraypackage(moves[1:])
                speak(chessconnection,packmoves)
            else:
                print("Opponent's turn...")
                board.asciiboard(sidecolor)
                packoppmoves = listen(chessconnection)
                oppmoves = arrayunpackage(packoppmoves)
                for i in range(4):
                    oppmoves[i] = int(oppmoves[i])
                square = board.square[oppmoves[0]][oppmoves[1]]
                square.moveme([oppmoves[2],oppmoves[3]],oppmoves[4])
                os.system('cls' if os.name == 'nt' else 'clear')
                try: winsound.PlaySound("SystemExclamation",winsound.SND_ASYNC | winsound.SND_LOOP)
                except: pass
            ##Rotate turn
            turncolor = (turncolor+1)%2
        input("Game over")
    except LostComs:
        chessconnection.close()
        input("Lost communication... continuing to single sided play.")
        gamecycleUNISIDE(turncolor)

def gamecycleUNISIDE(startcolor): ##The place the client and host send the game after losing comunication
    global colors
    while True:
        ##The 'end' variable is a message for the end of the game
        end = board.turn(startcolor)[0]##Ignores muliplayer responces
        if end != "":
            input(end)
            if end == "Checkmate":
                input(colors[(startcolor+1)%2] + " wins")
                break
        startcolor = (startcolor+1)%2
    input("(To leave press enter 1 last time.)")

asknotation()
#test()

##The code below starts the game
if not(multi): ##no modules to do multiplayer
    gamecycleHOTSEAT()

else: ##modules are present
    if choose2("Multiplayer?","y","n",1) == "y":
        if choose2("Host or client","h","c",1) == "h": ##Host
            HOST = socket.gethostbyname(socket.gethostname())
            print("Ip: "+ str(HOST))
            PORT = (input("Port: "))
            while not(PORT.isdigit()):
                PORT = (input("Port (MUST BE A NUMBER): "))
            PORT = int(PORT)
            
            try:
                chesssocket = hostme(HOST,PORT)
                chessconnection = chesssocket.connection
                gamecycleSIDEHOST()
            except Exception as e:
                input("There was an issue... >> " + str(e))
                gamecycleHOTSEAT()#$go to the gamecycleUNISIDE
        
        else: ##Client
            HOST = input("Ip: ")
            PORT = (input("Port: "))
            while not(PORT.isdigit()):
                PORT = (input("Port (MUST BE A NUMBER): "))
            PORT = int(PORT)
            try:
                chesssocket = clientme(HOST,PORT)
                chessconnection = chesssocket.clientsocket
                gamecycleSIDECLIENT()
            except Exception as e:
                input("There was an issue... >> " + str(e))
                gamecycleHOTSEAT()#$go to the gamecycleUNISIDE
    
    else: ##not multiplayer
        gamecycleHOTSEAT()
