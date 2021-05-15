from abc import get_cache_token
from graphics import *
from enum import Enum
from time import sleep

FILE = ["a", "b", "c", "d", "e", "f", "g", "h"]
ASSETLOCATION = "Assets/"

def makeRectangle(x1, y1, x2, y2, width):
    rect = Rectangle(Point(x1, y1), Point(x2, y2))
    rect.setWidth(width)
    return rect
def makeLine(x1, y1, x2, y2, width):
    line = Line(Point(x1, y1), Point(x2, y2))
    line.setWidth(width)
    return line
def makeCircle(x, y, radius ,width):
    cir = Circle(Point(x, y), radius)
    cir.setWidth = width
    return cir

class WindowWidthTooSmall(Exception): pass
class WindowHeightTooSmall(Exception): pass
class IncorrectFileInput(Exception): pass
class IncorrectRankInout(Exception): pass
class SquareHasNoPiece(Exception): pass
class InvalidPieceName(Exception): pass

class Color(Enum):
    White = 0
    Black = 1
class ChessPiece(Enum):
    Pawn = 1
    Knight = 2
    Bishop = 3
    Rook = 4
    Queen = 5
    King = 6
class PawnMoveDirection(Enum):
    Forward = 1
    Backward = -1

class Piece():
    def __init__(self, color, piece, img):
        self.color = color
        self.piece = piece
        self.img = img

    def draw(self, window) -> None:
        self.img.draw(window)

    def getColor(self) -> Color:
        return self.color
        
    def undraw(self) -> None:
        self.img.undraw()

    def __eq__(self, other) -> bool:
        try:
            return self.piece == other
        except:
            return False

    def getPiece(self) -> ChessPiece:
        return self.piece

    def isWhite(self) -> bool:
        return self.color == Color.White

class Square:
    def __init__(self, color, name, square):
        self.color = color
        self.name = name
        self.square = square
        self.centerPoint = Point((square.getP1().getX() + square.getP2().getX()) / 2,
            (square.getP1().getY() + square.getP2().getY()) / 2)
        self.piece = None
        self.window = None
        self.previewImg = None
    
    def drawSquare(self, window) -> None:
        self.window = window
        self.square.draw(window)

    def _setPiece(self, pieceName) -> None:
        if self.piece != None: self.removePiece()
        pieceColor = Color.Black if pieceName[0:5] == "Black" else Color.White
        pieceName = pieceName[5:]

        if pieceName == "Pawn":
            self.setPiece(ChessPiece.Pawn, pieceColor)
        elif pieceName == "Knight":
            self.setPiece(ChessPiece.Knight, pieceColor)
        elif pieceName == "Bishop":
            self.setPiece(ChessPiece.Bishop, pieceColor)
        elif pieceName == "Rook":
            self.setPiece(ChessPiece.Rook, pieceColor)
        elif pieceName == "Queen":
            self.setPiece(ChessPiece.Queen, pieceColor)
        elif pieceName == "King":
            self.setPiece(ChessPiece.King, pieceColor)
        else : raise InvalidPieceName

    def setPiece(self, piece: ChessPiece, pieceColor: Color) -> None:
        if self.piece != None: self.removePiece()

        img = Image(self.centerPoint, ASSETLOCATION + pieceColor.name + piece.name + ".gif")
        self.piece = Piece(pieceColor, piece, img)

        self.DrawPiece()

    def getPiece(self) -> Piece:
        return self.piece

    def DrawPiece(self) -> None:
        self.piece.draw(self.window)

    def removePiece(self) -> None:
        if self.piece == None: 
            raise SquareHasNoPiece
        else: 
            self.piece.undraw()
            self.piece = None
    
    def addPreview(self) -> None:
        self.previewImg = Circle(self.centerPoint, 5)
        self.previewImg.setWidth(2)
        self.previewImg.setOutline("blue")
        self.previewImg.draw(self.window)

    def removePreview(self) -> None:
        self.previewImg.undraw()
        self.previewImg = None

    def getCenterPoint(self) -> Point:
        return self.centerPoint
    
    def getName(self) -> str:
        return self.name
    
    def isEmpty(self) -> bool:
        return self.piece is None
    
    def getCoords(self) -> tuple :
        file = FILE.index(self.name[0])
        rank = 7 - int(self.name[1]) - 1 # offset if because of list start with 0 and not 1
        return file, rank

    def getColor(self) -> Color:
        return self.color

class Chess:
    board = {}

    def __init__(self, window):
        self.borderOffset = 50
        self.height = window.getHeight() - self.borderOffset
        self.width = window.getWidth() - self.borderOffset
        self.previewSquares = []
        self.window = window
        self.squareSize = (self.height - self.borderOffset) / 8

        if self.height <= 100:
            raise WindowHeightTooSmall
        if self.width <= 100:
            raise WindowWidthTooSmall

    def setUpBoard(self) -> None:
        global FILE
        border = makeRectangle(self.borderOffset, self.borderOffset, self.height, self.width, 7)
        border.draw(self.window)
        
        currentColor = Color.White
        for file in range(8):
            fileName = FILE[file]
            currentColor = (Color.Black if currentColor == Color.White else Color.White)
            self.board[fileName] = []
            for rank in range(7, -1, -1): #for loop has to be done like this because (0,0) is top right not bottom right
                rect = makeRectangle(file * self.squareSize + self.borderOffset, 
                    rank * self.squareSize + self.borderOffset,
                    (file + 1) * self.squareSize + self.borderOffset,
                    (rank + 1) * self.squareSize + self.borderOffset, 1)

                self.board[fileName].append(Square(currentColor, fileName + str(rank - 1), rect))
                rect.setFill("lime") if currentColor == Color.White else rect.setFill("gray")
                currentColor = (Color.Black if currentColor == Color.White else Color.White)

                self.board[fileName][-1].drawSquare(self.window)
                #sleep(0.01)

    def getBoard(self) -> dict:
        return self.board

    def _addPiece(self, pieceName, location) -> None:
        global ASSETLOCATION

        try:
            file = str(list(location)[0])
        except:
            raise IncorrectFileInput  

        try:  
            rank = int(list(location)[1])
        except: 
            raise IncorrectRankInout

        square = self.board[file][rank - 1]
        square._setPiece(pieceName)

    def setUpPieces(self) -> None:
        self._addPiece("WhiteRook", "a1")
        self._addPiece("WhiteRook", "h1")
        self._addPiece("WhiteKnight", "b1")
        self._addPiece("WhiteKnight", "g1")
        self._addPiece("WhiteBishop", "c1")
        self._addPiece("WhiteBishop", "f1")
        self._addPiece("WhiteQueen", "d1")
        self._addPiece("WhiteKing", "e1")

        for file in range(8):
            self._addPiece("WhitePawn", FILE[file] + "2")

        self._addPiece("BlackRook", "a8")
        self._addPiece("BlackRook", "h8")
        self._addPiece("BlackKnight", "b8")
        self._addPiece("BlackKnight", "g8")
        self._addPiece("BlackBishop", "c8")
        self._addPiece("BlackBishop", "f8")
        self._addPiece("BlackQueen", "d8")
        self._addPiece("BlackKing", "e8")

        for file in range(8):
            self._addPiece("BlackPawn", FILE[file] + "7")
    
    def movePiece(self, square1, square2) -> None:
        square2.setPiece(square1.piece.getPiece(), square1.piece.getColor())
        square1.removePiece()
   
    def makeMove(self) -> None:
        lastSelectedSquare = None
        selectedSquare = None
        moveColor = Color.White
        while(True):
            click = self.window.getMouse()
            x, y = self.getClickSquare(click)
            lastSelectedSquare = selectedSquare
            selectedSquare = self.board[FILE[x]][y]

            if selectedSquare in self.previewSquares:
                self.movePiece(lastSelectedSquare, selectedSquare)
                self.undrawPreviews()
                moveColor = Color.Black if selectedSquare.getPiece().isWhite() else Color.White
                self.undrawPreviews
                
            try:
                if selectedSquare.getPiece().getColor() != moveColor:
                    selectedSquare = lastSelectedSquare
                    continue
                    
            except:
                pass

            if len(self.previewSquares) != 0: 
                self.undrawPreviews()
                if selectedSquare != lastSelectedSquare: continue

            legalMoves = self.getAllLegalMoves(x, y)
            self.drawPreviews(legalMoves)
      
    def getClickSquare(self, click) -> tuple:
        clickX = click.getX() - self.borderOffset
        clickY = click.getY() - self.borderOffset
        if (clickX <= 0 or clickX <= 0 or clickX >= self.height - self.borderOffset or clickY >= self.width - self.borderOffset):
            print("Click is not inside chess board")
            return -1, -1
            
        x = int(clickX / self.squareSize) 
        y = 7 - int(clickY / self.squareSize) 

        return x, y

    def getAllLegalMoves(self, *coords) -> list:
        file, rank = coords
        currentSquare = self.board[FILE[file]][rank]
        currentPiece = currentSquare.getPiece()
        if currentSquare.isEmpty(): return []

        legalMoves = []
        if currentPiece == ChessPiece.Pawn:
            moveDirection = PawnMoveDirection.Forward if currentPiece.isWhite() else PawnMoveDirection.Backward
            if (currentPiece.isWhite() and rank == 1) or (not currentPiece.isWhite() and rank == 6):
                maxDistance = 2
            else: maxDistance = 1

            for change in range(1, 1 + maxDistance):
                
                try:     
                    possibleMove = self.board[FILE[file]][rank + change * moveDirection.value]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    else: 
                        break
                except:
                    pass

            try:     
                possibleMove = self.board[FILE[file + 1]][rank + 1 * moveDirection.value]
                if currentPiece.getColor() != possibleMove.getPiece().getColor():
                    legalMoves.append(possibleMove) 
            except:
                pass

            try:     
                possibleMove = self.board[FILE[file - 1]][rank + 1 * moveDirection.value]
                if currentPiece.getColor() != possibleMove.getPiece().getColor():
                    legalMoves.append(possibleMove) 
            except:
                pass

        elif currentPiece == ChessPiece.Knight:
            KnightMoves = [[1, 2], [-1 , 2] ,[1, -2], [-1, -2], [-2, 1], [-2, -1], [2, 1], [2, -1]]
            
            for change in KnightMoves:
                if file + change[0] < 0 or rank + change[1] < 0: continue
                try:     
                    possibleMove = self.board[FILE[file + change[0]]][rank + change[1]]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                except:
                    pass
    
        elif currentPiece == ChessPiece.Bishop:
            #++
            for change in range(1, 8):
                try:     
                    possibleMove = self.board[FILE[file + change]][rank + change]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove)
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass
            
            #+-
            for change in range(1, 8):
                if file - change < 0: continue
                try:     
                    possibleMove = self.board[FILE[file - change]][rank + change]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass

            #-+
            for change in range(1, 8):
                if rank - change < 0: continue
                try:     
                    possibleMove = self.board[FILE[file + change]][rank - change]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass
            
            #--
            for change in range(1, 8):
                if file - change < 0 or rank - change < 0: continue
                try:     
                    possibleMove = self.board[FILE[file - change]][rank - change]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass
        
        elif currentPiece == ChessPiece.Rook:
            #+
            for change in range(1, 8):
                try:     
                    possibleMove = self.board[FILE[file]][rank + change]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove)
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass
            
            #-
            for change in range(1, 8):
                if rank - change < 0: continue
                try:     
                    possibleMove = self.board[FILE[file]][rank - change]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass

            # +
            for change in range(1, 8):
                try:     
                    possibleMove = self.board[FILE[file + change]][rank]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass
            
            # -
            for change in range(1, 8):
                if file - change < 0: continue
                try:     
                    possibleMove = self.board[FILE[file - change]][rank]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass

        elif currentPiece == ChessPiece.Queen:
            #++
            for change in range(1, 8):
                try:     
                    possibleMove = self.board[FILE[file + change]][rank + change]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove)
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass
            
            #+-
            for change in range(1, 8):
                if file - change < 0: continue
                try:     
                    possibleMove = self.board[FILE[file - change]][rank + change]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass

            #-+
            for change in range(1, 8):
                if rank - change < 0: continue
                try:     
                    possibleMove = self.board[FILE[file + change]][rank - change]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass
            
            #--
            for change in range(1, 8):
                if file - change < 0 or rank - change < 0: continue
                try:     
                    possibleMove = self.board[FILE[file - change]][rank - change]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass

            #+
            for change in range(1, 8):
                try:     
                    possibleMove = self.board[FILE[file]][rank + change]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove)
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass
            
            #-
            for change in range(1, 8):
                if rank - change < 0: continue
                try:     
                    possibleMove = self.board[FILE[file]][rank - change]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass

            # +
            for change in range(1, 8):
                try:     
                    possibleMove = self.board[FILE[file + change]][rank]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass
            
            # -
            for change in range(1, 8):
                if file - change < 0: continue
                try:     
                    possibleMove = self.board[FILE[file - change]][rank]
                    if possibleMove.isEmpty():
                        legalMoves.append(possibleMove) 
                    elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                        legalMoves.append(possibleMove) 
                        break
                    else: 
                        break
                except:
                    pass

        elif currentPiece == ChessPiece.King:
            for xMove in range(-1, 2):
                for yMove in range(-1, 2):
                    if (file + xMove < 0) or (rank + yMove < 0) or (xMove == 0 and yMove == 0): continue
                    try:     
                        possibleMove = self.board[FILE[file + xMove]][rank + yMove]
                        if possibleMove.isEmpty():
                            legalMoves.append(possibleMove) 
                        elif currentPiece.getColor() != possibleMove.getPiece().getColor():
                            legalMoves.append(possibleMove) 
                    except:
                        pass
        return legalMoves

    def drawPreviews(self, legalMoves) -> None:
        self.previewSquares = legalMoves
        for square in legalMoves:
            square.addPreview()

    def undrawPreviews(self) -> None:
        for preview in self.previewSquares:
            preview.removePreview()
        
        self.previewSquares = []

    def clone(self) -> object:
        return self.copy()
        
    def _clickPrint(self) -> None:
        while(True):
            click = self.window.getMouse()
            clickX = click.getX() - self.borderOffset
            clickY = click.getY() - self.borderOffset
            if (clickX <= 0 or clickX <= 0 or clickX >= self.height - self.borderOffset or clickY >= self.width - self.borderOffset):
                print("not inside")
                continue
            
            coordX = int(clickX / self.squareSize) * self.squareSize + self.borderOffset + (self.squareSize / 2)
            coordY = int(clickY / self.squareSize) * self.squareSize + self.borderOffset + (self.squareSize / 2)
            cir = Circle(Point(coordX, coordY), 5)
            cir.setFill("green")
            cir.draw(self.window)

def main():
    window = GraphWin("Chess Board", 700, 700)
    chess = Chess(window)
    chess.setUpBoard()
    chess.setUpPieces()
    chess.makeMove()
    window.getMouse()

main()
