from decimal import getcontext, Decimal
from Messages import Messages

def logg(x):
    if x==0:
        return Decimal(0)
    else:
        return Decimal(x).ln()
        
def expp(x):
    return Decimal(x).exp()

class DataProcessor:
    def __init__(self):
        pass
        
    def inputParameters(self, experimentalData, startTerm, endTerm, k, precision, tolerance):
        getcontext().prec = precision
        self.toleranceRound = precision - tolerance
        def removeConstants(experimentalData, k):
            #If the input data is constant, do not remove constant
            isConstant = True #<HEURISTIC> Constant check
            for i in range(0, len(experimentalData) - 1):
                if experimentalData[i] != experimentalData[i+1]:
                    isConstant = False
                    break
            if isConstant:
                seqRemovedConstants = experimentalData
            #Else, subtracting each term by a value such that the first term has the value of k
            else:
                seqRemovedConstants = []
                for n in range(0, len(experimentalData)):
                    seqRemovedConstants += [Decimal(experimentalData[n]) -
                                            Decimal(experimentalData[0]) + Decimal(k)]
            return seqRemovedConstants
        self.a = removeConstants(experimentalData, k)
        self.startTerm = startTerm
        self.endTerm = endTerm
        
    def chooseMinimalErrorTerm(self, term, assumeContinuous): #<HEURISTIC> Choose highest valid terms
        if assumeContinuous:
            if term < 3:
                return [None, None, None]
            else:
                return [term, term-1, term-2]
        else:
            maxPoints = filter(lambda o: o <= term, self.discontinuities)
            if len(maxPoints) < 3:
                return [None, None, None]
            else:
                return [maxPoints[-1], maxPoints[-2], maxPoints[-3]]
            
    def calculateAsymptoticApproximations(self, assumeContinuous):
        #Calculate e, p, c, enl, pnl, and cnl approximations
        self.e = []
        self.p = []
        self.c = []
        self.enl = []
        self.pnl = []
        self.cnl = []
        for term in range(self.startTerm, self.endTerm):
            optimalTerms = self.chooseMinimalErrorTerm(term, assumeContinuous)
            n = optimalTerms[0]
            m = optimalTerms[1]
            l = optimalTerms[2]
            print "Calculating {}th EPC approximation using {}...".format(term, optimalTerms)
            try:
                #Store all repeated logarithm calculation for optimization
                Lan = logg(self.a[n])
                Lam = logg(self.a[m])
                Lal = logg(self.a[l])
                Ln = logg(n)
                Lm = logg(m)
                Ll = logg(l)
                LLn = logg(Ln)
                LLm = logg(Lm)
                LLl = logg(Ll)
                e = expp(((Lm-Ll)*(Lan-Lam+LLm-LLn)-(Ln-Lm)*(Lam-Lal+LLl-LLm))/
                         ((Ln-Lm)*(l-m)-(Lm-Ll)*(m-n)))
                p = (((m-l)*(Lan-Lam+LLm-LLn)-(n-m)*(Lam-Lal+LLl-LLm))/
                    ((n-m)*(Ll-Lm)-(m-l)*(Lm-Ln)))
                c = expp(((l*Lm-m*Ll)*(m*(Lan-LLn)-n*(Lam-LLm))-
                         (m*Ln-n*Lm)*(l*(Lam-LLm)-m*(Lal-LLl)))/
                         ((m*Ln-n*Lm)*(m-l)-(l*Lm-m*Ll)*(n-m)))
                enl = expp(((Lm-Ll)*(Lan-Lam)-(Ln-Lm)*(Lam-Lal))/
                           ((Ln-Lm)*(l-m)-(Lm-Ll)*(m-n)))
                pnl = (((m-l)*(Lan-Lam)-(n-m)*(Lam-Lal))/
                       ((n-m)*(Ll-Lm)-(m-l)*(Lm-Ln)))
                cnl = expp(((l*Lm-m*Ll)*(m*(Lan)-n*(Lam))-(m*Ln-n*Lm)*(l*(Lam)-m*(Lal)))/
                           ((m*Ln-n*Lm)*(m-l)-(l*Lm-m*Ll)*(n-m)))
                self.e += [e]
                self.p += [p]
                self.c += [c]
                self.enl += [enl]
                self.pnl += [pnl]
                self.cnl += [cnl]
            except Exception, e: #Need a suitable place holder value regardless the error
                print Messages.ERR_MATH_REPLACE, e
                self.e += [Decimal(0.0)]
                self.p += [Decimal(0.0)]
                self.c += [Decimal(0.0)]
                self.enl += [Decimal(0.0)]
                self.pnl += [Decimal(0.0)]
                self.cnl += [Decimal(0.0)]
                pass
        if assumeContinuous:
            self.checkForDiscontinuities()
            print "Found discontinuities preceding points: {}".format(self.discontinuities)
            if len(self.discontinuities) > 2:
                print("More than 2 discontinuities detected. " +
                      "Repeating calculations using discontinuities...")
                self.cont_e = self.e
                self.cont_p = self.p
                self.cont_c = self.c
                self.cont_enl = self.enl
                self.cont_pnl = self.pnl
                self.cont_cnl = self.cnl
                self.calculateAsymptoticApproximations(False)
        else:
            self.compareContDiscontApprox()
            if not self.aroundDiscontinuities:#Restore continuous case approximation
                self.e = self.cont_e
                self.p = self.cont_p
                self.c = self.cont_c
                self.enl = self.cont_enl
                self.pnl = self.cont_pnl
                self.cnl = self.cont_cnl
        self.determineHasLog()
    
    def compareContDiscontApprox(self):#<HEURISTIC> Chooses between approximations calculated around continuous and discontinuous points
        cont_epc = 0
        discont_epc = 0
        for n in range(0, self.endTerm):
            try:
                print "Choosing between continuous and discontinuous solutions for the {}th approximation...".format(n)
                #Evaluates the approximations of the two cases and checks which one is closer
                cont_epc = self.cont_e[-1]**n * n**self.cont_p[-1] * self.cont_c[-1] * logg(n)
                cont_epcnl = self.cont_enl[-1]**n * n**self.cont_pnl[-1] * self.cont_cnl[-1]
                discont_epc = self.e[-1]**n * n**self.p[-1] * self.c[-1] * logg(n)
                discont_epcnl = self.enl[-1]**n * n**self.pnl[-1] * self.cnl[-1]
                errorCont = (Decimal(self.a[n]) - cont_epc).copy_abs()
                errorContnl = (Decimal(self.a[n]) - cont_epcnl).copy_abs()
                errorDiscont = (Decimal(self.a[n]) - discont_epc).copy_abs()
                errorDiscontnl = (Decimal(self.a[n]) - discont_epcnl).copy_abs()
                if(self.roundOff(errorCont, self.toleranceRound) > 
                   self.roundOff(errorDiscont, self.toleranceRound)):
                    self.discontCount += 1
                else:
                    self.contCount += 1
                if(self.roundOff(errorContnl, self.toleranceRound) > 
                   self.roundOff(errorDiscontnl, self.toleranceRound)):
                    self.discontCount += 1
                else:
                    self.contCount += 1
            except Exception, e: #If no reasonable value could be calculated, ignore approximation
                print Messages.ERR_MATH_IGNORE, e
                pass
        self.aroundDiscontinuities = (self.discontCount > self.contCount)
    
    def checkForDiscontinuities(self):#<HEURISTIC> Looks for discontinuities/sudden jumps
        n = 3
        while n < self.endTerm:
            try:
                print "Checking for discontinuity before the {}th epc approximations".format(n)
                if not -(self.c[n+1]-self.c[n-1]).copy_abs() <= self.c[n] <= self.c[n-1]+self.c[n+1]:
                    self.discontinuities += [n]
                    n += 2 #skip the rest of discontinuous approximations
            except Exception, e: #If no reasonable value could be calculated, ignore approximation
                print Messages.ERR_MATH_IGNORE, e
                pass
            n += 1
        
    def determineHasLog(self):
        logCount = 0 #<HEURISTIC> Logarithm factor check
        noLogCount = 0
        if self.aroundDiscontinuities:
            loop = self.discontinuities
        else:
            loop = range(0, self.endTerm)
        for n in loop:
            try:
                print "Determining hasLog for the {}th term...".format(n)
                #Evaluates the approximations of the two cases and checks which one is closer
                errorNoLog = (Decimal(self.a[n]) -
                              (self.enl[-1]**n * n**self.pnl[-1] * self.cnl[-1])).copy_abs()
                errorLog = (Decimal(self.a[n]) -
                            (self.e[-1]**n * n**self.p[-1] * self.c[-1] * logg(n))).copy_abs()
                if(self.roundOff(errorNoLog, self.toleranceRound) > 
                   self.roundOff(errorLog, self.toleranceRound)):
                    logCount += 1
                else:
                    noLogCount += 1
            except Exception, e: #If no reasonable value could be calculated, ignore approximation
                print Messages.ERR_MATH_IGNORE, e
                pass
        self.hasLogPercent = "{}%".format((100.0 * logCount / (logCount+noLogCount)))
        self.logtoNoLog = "{} : {}".format(logCount, noLogCount)
        self.hasLog = (logCount >= noLogCount)
            
    def verifyAsymptoticEquivalence(self):
        #Verifies asymptotic equivalence between input function and generated approximation
        self.limitRatios = [] #<HEURISTIC> Asymptotic equivalence checking
        convergeCount = 0
        divergeCount = 0
        #Generate limit ratios between frequency counts and e, p, c, and hasLog
        for n in range(0, self.endTerm):
            try:
                print "Generating {}th Limit Ratio...".format(n)
                if self.hasLog:
                    self.limitRatios += [Decimal(self.a[n]) / Decimal(self.e[-1]**n *
                                         n**self.p[-1] * self.c[-1] * logg(n))]
                else:
                    self.limitRatios += [Decimal(self.a[n]) /
                                         Decimal(self.enl[-1]**n * n**self.pnl[-1] * self.cnl[-1])]
            except Exception, e: #Need a suitable place holder value regardless the error
                print Messages.ERR_MATH_REPLACE, e
                self.limitRatios += [Decimal(0.0)]
                pass
        #Checks for modified distance between each term is decreasing and the terms approach 1
        for term in range(0, self.endTerm):
            try:
                optimalTerms = self.chooseMinimalErrorTerm(term, not self.aroundDiscontinuities)
                n = optimalTerms[0]
                m = optimalTerms[1]
                l = optimalTerms[2]
                print "Convergence check of {}th Limit Ratio using {}...".format(term, optimalTerms)
                if(self.roundOff((m * (self.limitRatios[n]-self.limitRatios[m])).copy_abs(),
                   self.toleranceRound) > self.roundOff((l * (self.limitRatios[m]-
                   self.limitRatios[l])).copy_abs(), self.toleranceRound)):
                    divergeCount += 1
                else:
                    convergeCount += 1
            except Exception, e: #If no reasonable value could be calculated, ignore approximation
                print Messages.ERR_MATH_IGNORE, e
                pass
        self.convergePercent = "{}%".format((100.0*convergeCount / (convergeCount+divergeCount)))
        self.convergeDivergeRatio = "{} : {}".format(convergeCount, divergeCount)
        self.converges = (convergeCount >= divergeCount)
            
    def generateEPCSequence(self):
        #Generate plot points for the e, p, c, and hasLog approximation
        self.epcSequence = []
        for n in range(0, self.endTerm):
            print "Calculating {}th EPC plot point...".format(n)
            try:
                if self.hasLog:
                    self.epcSequence += [self.e[-1]**n * n**self.p[-1] * self.c[-1] * logg(n)]
                else:
                    self.epcSequence += [self.enl[-1]**n * n**self.pnl[-1] * self.cnl[-1]]
            except Exception, e: #Need suitable place holder regardless the error
                print Messages.ERR_MATH_REPLACE, e
                self.epcSequence += [Decimal(0.0)]
                pass
                    
    def roundOff(self, decimalValue, decimalPlaces):
        try:
            return decimalValue.quantize(Decimal(10) ** -decimalPlaces, rounding = "ROUND_HALF_UP")
        except Exception, e: #If the number it too large to round off, do not round off
            print Messages.ERR_ROUND_OFF, e
            return decimalValue