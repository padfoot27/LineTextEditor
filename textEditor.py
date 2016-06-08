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
    undoCommand = "z";
    redoCommand = "zz";

    def __init__(self):
        self.numLines = 0
        self.text = []
        self.clipBoard = []
        self.commandStack = []
        self.deleteTextStack = []
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
        return n > maxLines 

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
            return TextEditor.invalidOperation
        
        self.text.insert(n - 1, insertText)
        self.numLines += 1

    def deleteLineAtN(self, n):
        if self.checkBounds(n) == TextEditor.invalidOperation:
            return TextEditor.invalidOperation
        
        self.text.pop(n - 1)
        self.numLines -= 1

    def deleteMultipleLines(self, n, m):
        if self.checkMultipleBounds(n,m) == TextEditor.invalidOperation:
            return TextEditor.invalidOperation
        
        self.text = self.text[0 : n - 1] + self.text[m : self.numLines]
        self.numLines -= m - n + 1

    def copyMultipleLines(self, n, m):
        if self.checkMultipleBounds(n,m) == TextEditor.invalidOperation:
            return TextEditor.invalidOperation
        
        self.clipBoard = self.text[n - 1 : m]

    def pasteAtN(self, n):
        if self.checkBounds(n) == TextEditor.invalidOperation:
            return TextEditor.invalidOperation
        
        self.text = self.text[0 : n] + self.clipBoard + self.text[n : self.numLines]
        self.numLines = len(self.text)
        
    def startTextEditor(self):

        while True:
            command = raw_input()
            lenCommand = len(command)

            if lenCommand == 0:
                print TextEditor.invalidOperation

            elif lenCommand == 1 and command == TextEditor.dispayContentCommand:
                self.displayText()

            elif lenCommand == 1 and command == TextEditor.undoCommand:
                pass
            
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

            elif command[0] == TextEditor.insertLineCommand:
                command = command.split(".")

                n = -1

                try:
                    n = int(command[1])
                except:
                    print TextEditor.invalidOperation
                    return

                self.insertLineAtN(command[2], n)
                
            
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

            elif command[0] == TextEditor.pasteCommand:
                
                command = command.split(".")
                
                n = -1 
                
                try:
                    n = int(command[1])

                except:
                    print TextEditor.invalidOperation

                self.pasteAtN(n)

            elif command == TextEditor.redoCommand:
                pass

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

            elif command[0 : 2] == TextEditor.deleteLineCommand and len(command.split(".")) == 3:
                
                command = command.split(".")

                try:
                    n = int(command[1])
                    m = int(command[2])

                except:
                    print TextEditor.invalidOperation
                    return

                self.deleteMultipleLines(n, m)

            else:
                print TextEditor.invalidOperation


string = "Python is a widely used high-level, general-purpose, interpreted, dynamic programming language. Its design philosophy emphasizes code readability, and its syntax allows programmers to express concepts in fewer lines of code than possible in languages such as C++ or Java. The language provides constructs intended to enable clear programs on both a small and large scale."

textEditor = TextEditor()
textEditor.wrapText(string)
textEditor.startTextEditor()



