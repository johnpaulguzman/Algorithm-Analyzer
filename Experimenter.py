import os
import sys
from Messages import Messages
from math import factorial, floor, ceil
from decimal import getcontext, Decimal

def log(x):
    if x==0:
        return Decimal(0)
    else:
        return Decimal(x).ln()
        
def exp(x):
    return Decimal(x).exp()
        
def pow(base, exponent):
    return Decimal(base)**Decimal(exponent)

class Experimenter:
    def __init__(self):
        sys.setrecursionlimit(sys.maxint)
        
    def inputParameters(self, algoFilePath, endTerm, precision):
        self.algoFilePath = algoFilePath
        self.endTerm = endTerm
        getcontext().prec = precision
    
    def augmentCode(self):
        #Augments freqCount increments in input code
        print "Augmenting code..."
        def makeSpace(whitespaceAmount):
            whitespaces = ""
            for i in range(0, whitespaceAmount):
                whitespaces += " "
            return whitespaces
        augmentedFileString = []
        try:
            with open(self.algoFilePath) as file:
                fileLines = file.read().splitlines()
        except Exception, e: #Raise problem in file handling
            print Messages.ERR_FILE, e
            raise Exception("FILE_ERROR")
        for fileIndex in range(0, len(fileLines)):
            currentLine = fileLines[fileIndex]
            noIndentLine = currentLine.lstrip()
            lineIndentAmount = len(currentLine) - len(noIndentLine)
            #Just copy if statements start with these keywords
            if(noIndentLine == "" or noIndentLine.startswith("#") or
               noIndentLine.startswith("def ") or noIndentLine.startswith("global ") or
               noIndentLine.startswith("else ") or noIndentLine.startswith("else:") or
               noIndentLine.startswith("else(")):
                augmentedFileString += [currentLine]
                #Give access to freqCount variable in new scope
                if noIndentLine.startswith("def "):
                    augmentedFileString += [makeSpace(lineIndentAmount+4) + "global freqCount"]
                continue #Skip adding freqCount increments
            #Add freqCount increment before statement execution
            augmentedFileString += [makeSpace(lineIndentAmount) + "freqCount += 1"]
            augmentedFileString += [currentLine]
            #Add additional freqCount increments inside loops for loop management instructions
            if(noIndentLine.startswith("for ") or noIndentLine.startswith("for(") or
               noIndentLine.startswith("while ") or noIndentLine.startswith("while(")):
                augmentedFileString += [makeSpace(lineIndentAmount+4) +
                                        "freqCount += 1"]
        fileDirectory = self.algoFilePath.split("\\")
        directoryLength = len(fileDirectory)
        directoryPath = "\\".join(fileDirectory[0:-1]) + "\\preprocessed\\"
        #Create folder if none currently exists
        if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)
        #Create and store augmented algorithm in new file
        self.augmentedAlgoFilePath = (directoryPath + "preprocessed_" +
                                      "\\".join(fileDirectory[directoryLength-1:directoryLength]))
        with open(self.augmentedAlgoFilePath, "w") as augmentedFile:
            for augmentedLine in augmentedFileString:
                print >> augmentedFile, augmentedLine
                
    def runAugmentedAlgorithm(self):
        #Runs augmented algorithm for various input sizes
        global freqCount
        self.seqFreqCount = []
        #Open and interpret input algorithm
        try:
            with open(self.augmentedAlgoFilePath) as inputCode:
                exec(inputCode.read(), globals())
        except Exception, e: #Raise problem in file compilation
            print Messages.ERR_COMPILE, e
            raise Exception("COMPILATION_ERROR")
        try: #Test if the algorithm is valid using a term
            freqCount = 0
            f(0)
        except Exception, e: #Raise problem in running the algorithm
            print Messages.ERR_ALGORITHM, e
            raise Exception("ALGORITHM_ERROR")
        for n in range(0, self.endTerm):
            freqCount = 0
            try:
                print "Generating {}th Frequency Count measurement; use Ctrl+C to stop.".format(n)
                f(n)
                self.seqFreqCount += [Decimal(freqCount)]
            except KeyboardInterrupt: #Continue to the other calculations when interrupted
                self.endTerm = len(self.seqFreqCount)
                return
            except Exception, e: #Need a suitable place holder value regardless the error
                print Messages.ERR_MATH_REPLACE, e
                self.seqFreqCount += [Decimal(0.0)]
                pass
    
    def runInputFunction(self, functionString):
        #Runs evaluates input function for various input sizes
        self.seqFreqCount = []
        try: #Test if the string is valid using a term; last term used to avoid indeterminates
            n = self.endTerm-1
            Decimal(eval(functionString))
        except Exception, e: #Raise problem in function string evaluation
            print Messages.ERR_FUNCTION, e
            raise Exception("FUNCTION_ERROR")
        for n in range(0, self.endTerm):
            try:
                print "Generating {}th function value... use Ctrl+C to stop.".format(n)
                self.seqFreqCount += [Decimal(eval(functionString))]
            except KeyboardInterrupt: #Continue to the other calculations when interrupted
                self.endTerm = len(self.seqFreqCount)
                return
            except Exception, e: #Need a suitable place holder value regardless the error
                print Messages.ERR_MATH_REPLACE, e
                self.seqFreqCount += [Decimal(0.0)]
                pass
                
    def runInputSequence(self, sequenceString):
        #Copies each term of the input sequence as Decimal
        self.seqFreqCount = []
        try: #Test if the input sequence is valid using a term
            Decimal(sequenceString[0])
        except Exception, e: #Raise problem in string evaluation
            print Messages.ERR_NUMBER, e
            raise Exception("NUMBER_ERROR")
        self.endTerm = len(sequenceString)
        for n in range(0, self.endTerm):
            try:
                print "Storing {}th element value... Press Ctrl+C to stop.".format(n)
                self.seqFreqCount += [Decimal(sequenceString[n])]
            except KeyboardInterrupt: #Continue to the other calculations when interrupted
                self.endTerm = len(self.seqFreqCount)
                return
            except Exception, e: #Need a suitable place holder value regardless the error
                print Messages.ERR_MATH_REPLACE, e
                self.seqFreqCount += [Decimal(0.0)]
                pass 