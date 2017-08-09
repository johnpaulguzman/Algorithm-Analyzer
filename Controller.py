from Experimenter import Experimenter
from DataProcessor import DataProcessor
from GUI import GUI
from Messages import Messages
import os

class Controller:
    def __init__(self):
        self.experimenter = Experimenter()
        self.dataProcessor = DataProcessor()
        self.gui = GUI()
        self.gui.addListener("computeButton", "clicked", self.compute)
        self.gui.addListener("computeFunctionButton", "clicked", self.compute)
        self.gui.addListener("computeSequenceButton", "clicked", self.compute)
        self.gui.addListener("graphButton", "clicked", self.graph)
        self.gui.addListener("viewInputButton", "clicked", self.viewInput)
        self.gui.addListener("roundOffSpinButton", "value-changed", self.roundOffSummary)
        self.gui.addListener("showAdvancedButton", "clicked", self.showAdvancedSettings)
        self.gui.addListener("hideAdvancedButton", "clicked", self.hideAdvancedSettings)
    
    def compute(self, widget):
        #Prepares all the parameters needed by the Experimenter
        os.system("cls")
        self.dataProcessor.discontinuities = []
        self.dataProcessor.aroundDiscontinuities = False
        self.dataProcessor.contCount = 0
        self.dataProcessor.discontCount = 0
        try:
            buttonText = widget.get_label()
            if "Algorithm" in buttonText:
                self.experimenter.inputParameters(self.gui.builder.get_object("algoFileChooser").get_filename(),
                                                  int(self.gui.builder.get_object("endTermText").get_text()),
                                                  int(self.gui.builder.get_object("precisionText").get_text()))
                self.experimenter.augmentCode()
                self.experimenter.runAugmentedAlgorithm()    
            elif "F(n)" in buttonText:
                self.experimenter.inputParameters("",
                                                  int(self.gui.builder.get_object("endTermText").get_text()),
                                                  int(self.gui.builder.get_object("precisionText").get_text()))
                self.experimenter.runInputFunction(self.gui.builder.get_object("functionText").get_text())
            elif "Sequence" in buttonText:
                textBuffer = self.gui.builder.get_object("inputSequenceTextView").get_buffer()
                self.experimenter.inputParameters("",
                                                  int(self.gui.builder.get_object("endTermText").get_text()),
                                                  int(self.gui.builder.get_object("precisionText").get_text()))
                self.experimenter.runInputSequence(textBuffer.get_text(textBuffer.get_start_iter(),
                                                   textBuffer.get_end_iter()).split("\n"))
            self.runCalculations()
            self.displayToGUI()
        except Exception, e:
            print "An error has occurred while running experiments. ", e
            pass
        
    def runCalculations(self):
        #Prepares all the parameters needed by the DataProcessor and executes the calculations
        self.dataProcessor.inputParameters(self.experimenter.seqFreqCount,
                                           0, self.experimenter.endTerm,
                                           float(self.gui.builder.get_object("kText").get_text()),
                                           int(self.gui.builder.get_object("precisionText").get_text()),
                                           int(self.gui.builder.get_object("toleranceText").get_text()))
        self.dataProcessor.calculateAsymptoticApproximations(True)
        self.dataProcessor.verifyAsymptoticEquivalence()
        self.dataProcessor.generateEPCSequence()
   
    def displayToGUI(self):
        #Clears all previous text and displays new calculated values in GUI
        self.gui.setText("hasLogText", [self.dataProcessor.hasLog])
        self.gui.setText("hasLogPercentText", [self.dataProcessor.hasLogPercent])
        self.gui.setText("hasLogRatioText", [self.dataProcessor.logtoNoLog])
        self.gui.setText("convergesText", [self.dataProcessor.converges])
        self.gui.setText("convergesPercentText", [self.dataProcessor.convergePercent])
        self.gui.setText("convergesRatioText", [self.dataProcessor.convergeDivergeRatio])        
        self.gui.setText("seqFreqCountTextView", [self.experimenter.seqFreqCount])
        self.gui.setText("seqRemovedConstantsTextView", [self.dataProcessor.a])
        self.gui.setText("enlTextView", self.dataProcessor.enl)
        self.gui.setText("pnlTextView", self.dataProcessor.pnl)
        self.gui.setText("cnlTextView", self.dataProcessor.cnl)
        self.gui.setText("eTextView", self.dataProcessor.e)
        self.gui.setText("pTextView", self.dataProcessor.p)
        self.gui.setText("cTextView", self.dataProcessor.c)
        self.gui.setText("limitRatiosTextView", self.dataProcessor.limitRatios)
        self.roundOffSummary(self.gui.builder.get_object("roundOffSpinButton"))
        print "Finished!"
###############################################################################
        """ testing codes
        import sys
        import ntpath
        from contextlib import contextmanager
        from pprint import pprint

        def path_leaf(path):
            head, tail = ntpath.split(path)
            return tail or ntpath.basename(head)

        @contextmanager
        def stdout_redirected(new_stdout):
            save_stdout = sys.stdout
            sys.stdout = new_stdout
            try:
                yield None
            finally:
                sys.stdout = save_stdout

        data_name = "data_" + path_leaf(self.gui.builder.get_object("algoFileChooser").get_preview_filename())
        data_dict = self.dataProcessor.__dict__
        with open(data_name + ".txt", "w") as f:
            with stdout_redirected(f): # TODO add csv output
                pprint(data_dict)
        import code; code.interact(local=dict(globals(), **locals()))

from matplotlib.pyplot import plot, xlabel, ylabel, title, legend, show, ylim, xticks
c = data_dict['cont_c']
plot(range(len(c)), c, label = "Continuous C Approximation", marker = "o", linestyle = "--",)
ylim([-5, 125])
xlabel("n Value")
ylabel("C approximations calculated around n")
title("C approximations for the continuous case of Log2")
xticks(range(0,len(c),5))
show()
################################
for i in range(0, data_dict['endTerm']):
    if data_dict.get('aroundDiscontinuities'):
        (e,p,c) = (data_dict['cont_e'][i],data_dict['cont_p'][i],data_dict['cont_c'][i]) if data_dict['hasLog'] else (data_dict['cont_enl'][i],data_dict['cont_pnl'][i],data_dict['cont_cnl'][i])
    else:
        (e,p,c) = (data_dict['e'][i],data_dict['p'][i],data_dict['c'][i]) if data_dict['hasLog'] else (data_dict['enl'][i],data_dict['pnl'][i],data_dict['cnl'][i])
    print "="*20
    print i, data_dict['hasLog'], data_dict.get('aroundDiscontinuities')
    print "e=", e
    print "p=", p
    print "c=", c
    print "a=", data_dict['a'][i]
    try: 
        print e ** i * i ** p * c
        print data_dict['c'][i-1] <= c <= data_dict['c'][i+1]
    except Exception as e:
        print "0", e        
        """
###############################################################################
    
    def graph(self, widget):
        try:
            self.gui.createGraph(self.experimenter.seqFreqCount, self.dataProcessor.epcSequence)
        except AttributeError:
            print Messages.ERR_GRAPH
        
    def showAdvancedSettings(self, widget):
        self.gui.builder.get_object("advancedWindow").show()
        
    def hideAdvancedSettings(self, widget):
        self.gui.builder.get_object("advancedWindow").hide()
        
    def viewInput(self, widget):
        try:
            os.system("notepad.exe " + self.gui.builder.get_object("algoFileChooser").get_filename())
        except TypeError, e:
            print Messages.ERR_FILE
        
    def roundOffSummary(self, widget):
        #Display and round off summary
        if self.dataProcessor.hasLog:
            e = self.dataProcessor.e[-1]
            p = self.dataProcessor.p[-1]
            c = self.dataProcessor.c[-1]
        else:
            e = self.dataProcessor.enl[-1]
            p = self.dataProcessor.pnl[-1]
            c = self.dataProcessor.cnl[-1]
        places = widget.get_value_as_int()
        self.gui.setText("outputSummaryTextView", [("e= {:f}\n" + 
                                                    "p= {:f}\n" +
                                                    "c= {:f}\n" +
                                                    "hasLog= {}\n" +
                                                    "no. of terms= {}\n" +
                                                    "discontinuities at= {}\n" +
                                                    "calculated with disconts.= {} ({} > {})"
                                                    ).format(self.dataProcessor.roundOff(e, places),
                                                             self.dataProcessor.roundOff(p, places),
                                                             self.dataProcessor.roundOff(c, places),
                                                             self.dataProcessor.hasLog,
                                                             self.experimenter.endTerm,
                                                             self.dataProcessor.discontinuities,
                                                             self.dataProcessor.aroundDiscontinuities,
                                                             self.dataProcessor.discontCount,
                                                             self.dataProcessor.contCount)])