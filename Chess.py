from graphics import *
from enum import Enum
import time

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
ASSETLOCATION = "Assets/"

def makeRectangle(x1, y1, x2, y2, width):
    rect = Rectangle(Point(x1, y1), Point(x2, y2))
    rect.setWidth(width)
    return rect
def makeLine(x1, y1, x2, y2, width):
    line = Line(Point(x1, y1), Point(x2, y2))
    line.setWidth(width)
    return line

class WindowWidthTooSmall(Exception): pass
class WindowHeightTooSmall(Exception): pass
class IncorrectFileInput(Exception): pass
class IncorrectRankInout(Exception): pass
class SquareHasNoPiece(Exception): pass
class InvalidPieceName(Exception): pass

class Colors(Enum):
    White = 0
    Black = 1

class _piece():
    def __init__(self, color):
        self.color = color

class _Pawn(_piece):
    def __init__(self, color):
        super().__init__(color)
        self.imageName = color.name + "Pawn"

    def getName(self):
        return self.imageName

class _Knight(_piece):
    def __init__(self, color):
        super().__init__(color)
class _Bishop(_piece):
    def __init__(self, color):
        super().__init__(color)
class _Rook(_piece):
    def __init__(self, color):
        super().__init__(color)
class _Queen(_piece):
    def __init__(self, color):
        super().__init__(color)
class _King(_piece):
    def __init__(self, color):
        super().__init__(color)

class _Square:
    def __init__(self, color, name, square):
        self.color = color
        self.name = name
        self.square = square
        self.centerPoint = Point((square.getP1().getX() + square.getP2().getX()) / 2,
            (square.getP1().getY() + square.getP2().getY()) / 2)
        self.piece = None
        self.window = None
    
    def drawSquare(self, window):
        self.window = window
        self.square.draw(window)

    def drawPiece(self, imageName):
        pieceColor = Colors.Black if imageName[0:5] == "Black" else Colors.White
        pieceName = imageName[5:]
        print(pieceName)
        
        if pieceName == "Pawn":
            self.peice = _Pawn(pieceColor)
        elif pieceName == "Knight":
            self.peice = _Knight(pieceColor)
        elif pieceName == "Bishop":
            self.peice = _Bishop(pieceColor)
        elif pieceName == "Rook":
            self.peice = _Rook(pieceColor)
        elif pieceName == "Queen":
            self.peice = _Queen(pieceColor)
        elif pieceName == "King":
            self.peice = _King(pieceColor)
        else : raise InvalidPieceName

        img = Image(self.centerPoint, ASSETLOCATION + imageName + ".gif")
        img.draw(self.window)

    def removePiece(self):
        if self.piece == None: raise SquareHasNoPiece
        else: self.piece = None
        
        self.drawSquare(self.window)

    def getName(self):
        return self.name

    def getColor(self):
        return self.color

class Chess:
    board = {}

    def __init__(self, window):
        self.borderOffset = 50
        self.height = window.getHeight() - self.borderOffset
        self.width = window.getWidth() - self.borderOffset
        self.window = window
        self.squareSize = (self.height - self.borderOffset) / 8

        if self.height <= 100:
            raise WindowHeightTooSmall
        if self.width <= 100:
            raise WindowWidthTooSmall

    def setUpBoard(self):
        global FILES
        border = makeRectangle(self.borderOffset, self.borderOffset, self.height, self.width, 7)
        border.draw(self.window)
        
        currentColors = Colors.Black
        for file in range(8):
            fileName = FILES[file]
            currentColors = (Colors.Black if currentColors == Colors.White else Colors.White)
            self.board[fileName] = []
            for rank in range(8):
                rect = makeRectangle(file * self.squareSize + self.borderOffset, 
                    rank * self.squareSize + self.borderOffset,
                    (file + 1) * self.squareSize + self.borderOffset,
                    (rank + 1) * self.squareSize + self.borderOffset, 1)

                self.board[fileName].append(_Square(currentColors, fileName + str(rank + 1), rect))
                rect.setFill("lime") if currentColors == Colors.White else rect.setFill("gray")
                currentColors = (Colors.Black if currentColors == Colors.White else Colors.White)

                self.board[fileName][rank].drawSquare(self.window)

                #time.sleep(0.025)

    def getBoard(self):
        return self.board

    def _addPiece(self, pieceName, location):
        global ASSETLOCATION
        print(list(location))
        try:
            file = str(list(location)[0])
        except:
            raise IncorrectFileInput  

        try:  
            rank = int(list(location)[1])
        except: 
            raise IncorrectRankInout

        self.board[file][rank - 1].drawPiece(pieceName)

    def _clickPrint(self):
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
            cir.setFill("white")
            cir.draw(self.window)

            print(str(coordX) + ", " + str(coordY))

def main():
    window = GraphWin("Chess Board", 700, 700)
    chess = Chess(window)
    chess.setUpBoard()
    chess._addPiece("BlackKnight", "e8")
    chess._clickPrint()
    window.getMouse()

main()
