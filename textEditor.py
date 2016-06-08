class TextEditor:
    
    invalidOperation = 'Invalid operation' 
    
    # Commands
    dispayContentCommand = "d";
    displaySpecificLinesCommand = "d."
    insertLineCommand = "i";
    deleteLineCommand = "dd";
    copyLineCommand = "y";
    copyLineCommandFull = "yy"
    pasteCommand = "p";
    undoCommandL = "z";
    redoCommandL = "zz";
    dot = "."
    insertMultipleLineCommand = "x";
    undo = True

    def __init__(self):
        self.numLines = 0
        self.text = []
        self.clipBoard = []
        self.commandStack = []
        self.redoStack = []
        self.deleteTextStackUndo = []
        self.deleteTextStackRedo = []
        self.lineLength = 45

    def wrapText(self, rawText):
        textLen = len(rawText)
        i = 0
        while i + self.lineLength < textLen:
            self.text.append(rawText[i : i + self.lineLength])
            i = i + self.lineLength
        
        self.text.append(rawText[i : textLen])
        self.numLines = len(self.text)
    
    def checkLowerBound(self, n):
        return n <= 0

    def checkUpperBound(self, n, maxLines):
        return n > maxLines + 1 

    def checkMultipleBounds(self, n, m):
        if (self.checkLowerBound(n) or self.checkUpperBound(m, self.numLines) or n > m):
            return TextEditor.invalidOperation
    
    def checkBounds(self, n):
        if (self.checkLowerBound(n) or self.checkUpperBound(n, self.numLines)):
            return TextEditor.invalidOperation

    def displayText(self):
        for i in xrange(self.numLines):
            print (str) (i + 1) + " " + self.text[i]

    def displaySpecificLines(self, n, m):
        if self.checkMultipleBounds(n,m) == TextEditor.invalidOperation:
            return TextEditor.invalidOperation

        for i in xrange(n - 1, m):
            print self.text[i]

    def insertLineAtN(self, insertText, n):
        if self.checkBounds(n) == TextEditor.invalidOperation:
            if not (self.numLines == 0 and n == 1):
                return TextEditor.invalidOperation
        
        if TextEditor.undo:
            self.commandStack.insert(0, TextEditor.deleteLineCommand + TextEditor.dot + str(n))
        else :
            self.redoStack.insert(0, TextEditor.deleteLineCommand + TextEditor.dot + str(n))
        self.text.insert(n - 1, insertText)
        self.numLines += 1

    def deleteLineAtN(self, n):
        if self.checkBounds(n) == TextEditor.invalidOperation:
            return TextEditor.invalidOperation
        if TextEditor.undo:
            self.commandStack.insert(0, TextEditor.insertLineCommand + TextEditor.dot + str(n) + TextEditor.dot + self.text[n - 1])
        else:
            self.redoStack.insert(0, TextEditor.insertLineCommand + TextEditor.dot + str(n) + TextEditor.dot + self.text[n - 1])
        self.text.pop(n - 1)
        self.numLines -= 1

    def deleteMultipleLines(self, n, m):
        if self.checkMultipleBounds(n,m) == TextEditor.invalidOperation:
            return TextEditor.invalidOperation
        
        if TextEditor.undo:
            self.commandStack.insert(0, TextEditor.insertMultipleLineCommand)
            self.deleteTextStackRedo.insert(0, (self.text[n - 1 : m], n))
        else :
            self.redoStack.insert(0, TextEditor.insertMultipleLineCommand)
            self.deleteTextStackUndo.insert(0, (self.text[n - 1 : m], n))

            
        self.text = self.text[0 : n - 1] + self.text[m : self.numLines]
        self.numLines -= m - n + 1
    
    def insertMultipleLines(self, n, text):

        if self.checkBounds(n) == TextEditor.invalidOperation:
            if not (self.numLines == 0 and n == 1):
                return TextEditor.invalidOperation
        
        if TextEditor.undo:
            self.commandStack.insert(0, TextEditor.deleteLineCommand + TextEditor.dot + str(n) + TextEditor.dot + str(n + len(text) - 1))
        else:
            self.redoStack.insert(0, TextEditor.deleteLineCommand + TextEditor.dot + str(n) + TextEditor.dot + str(n + len(text) - 1))

        self.text = self.text[0 : n - 1] + text + self.text[n - 1 : self.numLines]
        self.numLines = len(self.text)
    
    def copyMultipleLines(self, n, m):
        if self.checkMultipleBounds(n,m) == TextEditor.invalidOperation:
            return TextEditor.invalidOperation
        
        self.clipBoard = self.text[n - 1 : m]

    def pasteAtN(self, n):
        if (self.clipBoard == ""):
           return
        self.insertMultipleLines(n, self.clipBoard)

    def undoCommand(self):
        if len(self.commandStack) == 0:
            print TextEditor.invalidOperation
            return
        TextEditor.undo = False
        prevCommand = self.commandStack[0]
        self.commandStack.pop(0)
        
        self.executeCommand(prevCommand)

    def redoCommand(self):
        if len(self.redoStack) == 0:
            print TextEditor.invalidOperation
            return
        prevCommand = self.redoStack[0]
        self.redoStack.pop(0)

        self.executeCommand(prevCommand)
    
    def executeCommand(self, command):
        lenCommand = len(command)
        if lenCommand == 0:
            print TextEditor.invalidOperation
            TextEditor.undo = True
            

        elif lenCommand == 1 and command == TextEditor.dispayContentCommand:
            self.displayText()
            TextEditor.undo = True

        elif lenCommand == 1 and command == TextEditor.undoCommandL:
            self.undoCommand()
        
        elif lenCommand == 1 and command == TextEditor.insertMultipleLineCommand:
            
            if TextEditor.undo:
                n = self.deleteTextStackUndo[0][1]
                text = self.deleteTextStackUndo[0][0]
                self.deleteTextStackUndo.pop(0)
            else:
                n = self.deleteTextStackRedo[0][1]
                text = self.deleteTextStackRedo[0][0]
                self.deleteTextStackRedo.pop(0)
            
            self.insertMultipleLines(n, text)
            TextEditor.undo = True

        elif lenCommand < 2:
            print TextEditor.invalidOperation

        elif command[0 : 2] == TextEditor.displaySpecificLinesCommand:
            command = command.split(".")
            n = -1
            m = -1

            try:
                n = int(command[1])
                m = int(command[2])
            except:
                print TextEditor.invalidOperation

            self.displaySpecificLines(n , m)
            TextEditor.undo = True

        elif command[0] == TextEditor.insertLineCommand:
            command = command.split(".")

            n = -1

            try:
                n = int(command[1])
            except:
                print TextEditor.invalidOperation
                return

            self.insertLineAtN(command[2], n)
            TextEditor.undo = True
            
        
        elif command[0] == TextEditor.copyLineCommand:
            
            command = command.split(".")
            if command[0] != TextEditor.copyLineCommandFull:
                print TextEditor.invalidOperation
                return
            n = -1
            m = -1
            try :
                n = int(command[1])
                m = int(command[2])
            except:
                print TextEditor.invalidOperation
                return

            self.copyMultipleLines(n , m)
            TextEditor.undo = True

        elif command[0] == TextEditor.pasteCommand:
            
            command = command.split(".")
            
            n = -1 
            
            try:
                n = int(command[1])

            except:
                print TextEditor.invalidOperation

            self.pasteAtN(n)
            TextEditor.undo = True

        elif command == TextEditor.redoCommandL:
            self.redoCommand()
            TextEditor.undo = True

        elif lenCommand < 3:
            print TextEditor.invalidOperation

        elif command[0 : 2] == TextEditor.deleteLineCommand and len(command.split(".")) == 2:
            
            command = command.split(".")

            n = -1

            try:
                n = int(command[1])
            except:
                print TextEditor.invalidOperation
                return
            
            self.deleteLineAtN(n)
            TextEditor.undo = True

        elif command[0 : 2] == TextEditor.deleteLineCommand and len(command.split(".")) == 3:
            
            command = command.split(".")

            try:
                n = int(command[1])
                m = int(command[2])

            except:
                print TextEditor.invalidOperation
                return

            self.deleteMultipleLines(n, m)
            TextEditor.undo = True

        else:
            print TextEditor.invalidOperation
            TextEditor.undo = True


    def startTextEditor(self):

        while True:
            command = raw_input()
            if not (command == TextEditor.insertMultipleLineCommand):
                self.executeCommand(command)


string = "Python is a widely used high-level, general-purpose, interpreted, dynamic programming language Its design philosophy emphasizes code readability, and its syntax allows programmers to express concepts in fewer lines of code than possible in languages such as C++ or Java The language provides constructs intended to enable clear programs on both a small and large scale"

textEditor = TextEditor()
textEditor.wrapText(string)
textEditor.startTextEditor()



