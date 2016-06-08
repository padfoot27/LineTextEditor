class TextEditor:
    
    invalidOperation = 'Invalid operation' 

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

    def displayText(self):
        for i in xrange(self.numLines):
            print (str) (i + 1) + " " + self.text[i]

    def displaySpecificLines(self, n, m):
        if (self.checkLowerBound(n) or self.checkUpperBound(m, self.numLines)):
            return 'Invalid operation'

        return self.text[n - 1 : m]


string = "Python is a widely used high-level, general-purpose, interpreted, dynamic programming language. Its design philosophy emphasizes code readability, and its syntax allows programmers to express concepts in fewer lines of code than possible in languages such as C++ or Java. The language provides constructs intended to enable clear programs on both a small and large scale."

textEditor = TextEditor()
textEditor.wrapText(string)
textEditor.displayText()
print textEditor.displaySpecificLines(4,5)