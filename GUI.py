import pygtk  
pygtk.require('2.0')
import gtk  
import os
from matplotlib.pyplot import plot, xlabel, ylabel, title, legend, show

current_directory = os.path.split(os.path.abspath(__file__))[0]

class GUI:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(current_directory + "\\GUI.glade")
        self.builder.get_object("algoFileChooser").set_current_folder(current_directory + "\\experiments")
        self.builder.get_object("mainWindow").connect("destroy", gtk.main_quit)
        
    def addListener(self, widgetName, eventClass, action):
        self.builder.get_object(widgetName).connect(eventClass, action)
    
    def show(self):
        gtk.main()
    
    def quit(self, widget):
        sys.exit(0)  
        
    def setText(self, textFieldName, messages):
        #Prints text to a TextView or TextEntry widget
        widget = self.builder.get_object(textFieldName)
        doScrollDown = False
        #Clear previous TextView contents
        if type(widget) == gtk.TextView:
            textBuffer = widget.get_buffer()
            textBuffer.set_text("")
            #If the message is longer than 1 line, scroll down later
            if len(messages) > 1:
                doScrollDown = True
        for i in range(0, len(messages)):
            if i == len(messages) - 1:
                #If message is a list, dump list contents in a single line separated by a ", "
                if type(messages[i]) is list:
                    stringMessage = ""
                    for submessage in messages[i]:
                        stringMessage += str(submessage) + ", "
                else:
                    stringMessage = str(messages[i])
            #If the current iteration is the not last message, add new line
            else:
                stringMessage = str(messages[i]) + "\n"
            #Insert new message for different widgets
            if type(widget) == gtk.TextView:
                textBuffer.insert(textBuffer.get_end_iter(), stringMessage)
            elif type(widget) == gtk.Entry:
                widget.set_text(stringMessage)
        #Scroll down TextView
        if doScrollDown:
                textBuffer.insert(textBuffer.get_end_iter(), "\n")
                widget.scroll_to_mark(textBuffer.get_insert(), 0)
            
    def createGraph(self, plotFreqCount, plotEPC):
        #Plots the given two sets of points
        xaxis = range(0, len(plotFreqCount))
        plot(xaxis, plotEPC, label = "EPC Approximation")
        plot(xaxis, plotFreqCount, label = "Measured Frequency Count", marker = "o",
             linestyle = "--", color = "r")
        xlabel("Input size")
        ylabel("Frequency Counts")
        title("Time Complexity")
        legend()
        show()