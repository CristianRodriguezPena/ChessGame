from abc import get_cache_token
from graphics import *
from enum import Enum
from time import sleep

FILE = ["a", "b", "c", "d", "e", "f", "g", "h"]
ASSETLOCATION = "Assets/"

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
def swapColor(color: Color) -> Color:
        return Color.Black if color == Color.White else Color.White

class WindowWidthTooSmall(Exception): pass
class WindowHeightTooSmall(Exception): pass
class IncorrectFileInput(Exception): pass
class IncorrectRankInout(Exception): pass
class SquareHasNoPiece(Exception): pass
class InvalidPieceName(Exception): pass

class Piece():
    def __init__(self, color: Color, piece: ChessPiece, img):
        self.color = color
        self.chessPiece = piece
        self.img = img

    def draw(self, window: GraphWin) -> None:
        self.img.draw(window)

    def undraw(self) -> None:
        self.img.undraw()

    def __eq__(self, other) -> bool:
        try:
            return self.chessPiece == other
        except:
            return False

    def isWhite(self) -> bool:
        return self.color == Color.White

class Square:
    def __init__(self, color: Color, name: str, img: Image):
        self.color = color
        self.name = name
        self.file = self.name[0]
        self.rank = int(self.name[1]) 
        self.img = img
        self.centerPoint = Point((img.getP1().getX() + img.getP2().getX()) / 2,
            (img.getP1().getY() + img.getP2().getY()) / 2)
        self.piece = None
        self.window = None
        self.previewImg = None
        self.canCastle = False
    
    def drawSquare(self, window: GraphWin) -> None:
        self.window = window
        self.img.draw(window)

    def _setPiece(self, pieceName: str) -> None:
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

        self.canCastle = self.piece.chessPiece == ChessPiece.King or self.piece.chessPiece == ChessPiece.Rook

    def setPiece(self, piece: ChessPiece, pieceColor: Color) -> None:
        if self.piece != None: self.removePiece()

        img = Image(self.centerPoint, ASSETLOCATION + pieceColor.name + piece.name + ".gif")
        self.piece = Piece(pieceColor, piece, img)

        self._drawPiece()

    def previewPiece(self, piece: Piece) -> None:
        self.piece = piece

    def getPiece(self) -> Piece:
        return self.piece

    def _drawPiece(self) -> None:
        self.piece.draw(self.window)

    def removePiece(self) -> None:
        if self.piece == None: 
            raise SquareHasNoPiece
        else: 
            self.piece.undraw()
            self.piece = None
    
    def flashSquare(self, duration: float, color: str) -> None:
        flashSquare = Rectangle(Point(self.img.getP1().getX() + 5, self.img.getP1().getY() + 5), Point(self.img.getP2().getX() - 5, self.img.getP2().getY() - 5))
        flashSquare.setWidth(10)
        flashSquare.setOutline(color)

        flashSquare.draw(self.window)
        sleep(duration)
        flashSquare.undraw()
        sleep(duration)
        flashSquare.draw(self.window)
        sleep(duration)
        flashSquare.undraw()

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
    
    def isEmpty(self) -> bool:
        return self.piece is None


class Chess:
    board = {}

    def __init__(self, window: GraphWin):
        self.borderOffset = 50
        self.height = window.getHeight() - self.borderOffset
        self.width = window.getWidth() - self.borderOffset
        self.possibleMoves = []
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

                self.board[fileName].append(Square(currentColor, fileName + str(8 - rank), rect))
                rect.setFill("lime") if currentColor == Color.White else rect.setFill("gray")
                currentColor = (Color.Black if currentColor == Color.White else Color.White)

                self.board[fileName][-1].drawSquare(self.window)
                #sleep(0.01)

    def getBoard(self) -> dict:
        return self.board

    def _addPiece(self, pieceName: str, location: str) -> None:
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
    
    def movePiece(self, square1: Square, square2: Square) -> None:
        if square1.piece == ChessPiece.King and square1.canCastle:
            difference = FILE.index(square1.file) - FILE.index(square2.file)
            if abs(difference) > 1:
                rookMoveDistance = 1 if difference > 0 else -1
                rookSquare = self.board["a" if difference > 0 else "h"][square1.rank - 1]
                newRooksquare = self.board[FILE[FILE.index(square2.file) + rookMoveDistance]][square2.rank - 1]
                self.movePiece(rookSquare, newRooksquare)

        square2.setPiece(square1.piece.chessPiece, square1.piece.color)
        square1.removePiece()
        square1.canCastle = False
   
    def makeMove(self) -> None:
        lastSelectedSquare = None
        selectedSquare = None
        moveColor = Color.White
        while(True):
            click = self.window.getMouse()
            x, y = self.getClickSquare(click)
            lastSelectedSquare = selectedSquare
            selectedSquare = self.board[FILE[x]][y]

            if selectedSquare in self.possibleMoves:
                kingInCheck = self.isMoveAllowed(lastSelectedSquare, selectedSquare)
                if kingInCheck is None:
                    self.movePiece(lastSelectedSquare, selectedSquare)
                    self.undrawPreviews()
                    moveColor = swapColor(moveColor)
                    kingSquare = self.inCheck(moveColor)
                    if kingSquare is not None :
                        kingSquare.flashSquare(0.5, "red")

                        if self.checkForcheckmate(moveColor):
                            print(moveColor.name, "is in checkmate!")
                            break

                    self.undrawPreviews
                else: kingInCheck.flashSquare(0.5, "red")
                
            try:
                if selectedSquare.piece.color != moveColor:
                    selectedSquare = lastSelectedSquare
                    continue
                    
            except: pass

            if len(self.possibleMoves) != 0: 
                self.undrawPreviews()
                if selectedSquare != lastSelectedSquare: continue

            legalMoves = self.getAllLegalMoves(x, y)
            self.drawPreviews(legalMoves)
      
    def getClickSquare(self, click: Point) -> tuple:
        clickX = click.getX() - self.borderOffset
        clickY = click.getY() - self.borderOffset
        if (clickX <= 0 or clickX <= 0 or clickX >= self.height - self.borderOffset or clickY >= self.width - self.borderOffset):
            print("Click is not inside chess board")
            return -1, -1
            
        x = int(clickX / self.squareSize) 
        y = 7 - int(clickY / self.squareSize) 

        return x, y

    def getAllLegalMoves(self, *coords: tuple) -> list:
        file, rank = coords
        currentSquare = self.board[FILE[file]][rank]
        currentPiece = currentSquare.piece
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
                if currentPiece.color != possibleMove.piece.color:
                    legalMoves.append(possibleMove) 
            except:
                pass

            try:     
                possibleMove = self.board[FILE[file - 1]][rank + 1 * moveDirection.value]
                if currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                    elif currentPiece.color != possibleMove.piece.color:
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
                        elif currentPiece.color != possibleMove.piece.color:
                            legalMoves.append(possibleMove) 
                    except: pass

            if currentSquare.canCastle:
                try:
                    ARook = self.board["a"][rank]
                    if ARook.canCastle and (self.board["b"][rank].isEmpty() and self.board["c"][rank].isEmpty() and self.board["d"][rank].isEmpty()):
                        legalMoves.append(self.board["c"][rank])
                except: pass

                try:
                    HRook = self.board["h"][rank]
                    if HRook.canCastle and (self.board["f"][rank].isEmpty() and self.board["g"][rank].isEmpty()):
                        legalMoves.append(self.board["g"][rank])
                except: pass

        return legalMoves

    def isMoveAllowed(self, square1: Square, square2: Square) -> Square:
        lostPiece = square2.piece
        self.previewMove(square1, square2)
        kingSquare = self.inCheck(square2.piece.color)
        self.previewMove(square2, square1)
        square2.previewPiece(lostPiece)

        if kingSquare is not None and square1.piece.chessPiece == ChessPiece.King:
            kingSquare = square1        

        return kingSquare
            
    def drawPreviews(self, legalMoves: list) -> None:
        self.possibleMoves = legalMoves
        for square in legalMoves:
            square.addPreview()

    def undrawPreviews(self) -> None:
        for preview in self.possibleMoves:
            preview.removePreview()
        
        self.possibleMoves = []

    def previewMove(self, square1: Square, square2: Square):
        square2.previewPiece(square1.piece)
        square1.previewPiece(None)

    def inCheck(self, colorInCheck: Color) -> Square:
        checkingColor = swapColor(colorInCheck)

        kingInCheck = None
        for file in range(0, 8):
            for rank in range(0, 8):
                currentSquare = self.board[FILE[file]][rank]
                try:
                    if currentSquare.piece.color == checkingColor:
                        legalMoves = self.getAllLegalMoves(file, rank)
                        for moveSquare in legalMoves:
                            if moveSquare.piece == ChessPiece.King:
                                kingInCheck = moveSquare
                except:
                    pass

        return kingInCheck
    
    def checkForcheckmate(self, colorInCheck: Color) -> bool:
        checkingColor = swapColor(colorInCheck)

        for file in range(0, 8):
            for rank in range(0, 8):
                square = self.board[FILE[file]][rank]
                allMoves = self.getAllLegalMoves(file, rank)

                try:
                    if square.piece.color == colorInCheck:
                        for move in allMoves:
                            if self.isMoveAllowed(square, move) is None: return False
                except:
                    pass

        return True

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