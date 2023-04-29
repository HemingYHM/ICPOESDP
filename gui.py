#write a program with a gui that asks for two user imputs, one named Rawdata, one named dilution table. 
#Then it will save it to two variables, and apply dpUtil functions to it.

import tkinter as tk
from tkinter import filedialog
from tkinter import *
import pandas as pd
import dpUtil as dp
import calibrationTool as ct


def SelectRawData():
    """This function is called when the user clicks the button to select the raw data file.
      It opens a file dialog box and saves the file path to a global variable called rawData"""
    global rawData
    rawData = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    rawDataButton.config(text = str(rawData))


def SelectDilutionTable():
    """This function is called when the user clicks the button to select the dilution table file."""
    global dilutionTable
    dilutionTable = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    dilutionTableButton.config(text = str(dilutionTable))

def SelectPPMTableForCalibration():
    """This function is called when the user clicks the button to select the ppm table file."""
    global PPMTableForCalibration
    PPMTableForCalibration = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    PPMTableForCalibrationButton.config(text = str(PPMTableForCalibration))

def processData():
    """This function is called when the user clicks the button to process the data. It calls the workupData function from dpUtil.py"""
    #button that processes the data
    global table1, table2, table3
    table1, table2, table3 = dp.workupData(rawData, dilutionTable)
    processDataButton.config(text="Data Processed :D")

def exportToCSV(table1, table2, table3):
    """This function is called when the user clicks the button to export the data. It calls the exportToCSV function from dpUtil.py"""
    #button that asks for a directory to save the data to, and export the three tbales to csv files in that directory
    directory = filedialog.askdirectory()
    table1.to_csv(directory + "/avgAndStdDev.csv")
    table2.to_csv(directory + "/blankTable.csv")
    table3.to_csv(directory + "/ppmTable.csv")
    exportDataButton.config(text="Data Exported :D")

def graphCalibration(raw, PPM):
    """This function is called when the user clicks the button to graph the calibration. It calls the plotCalibrationCurve function from calibrationTool.py"""
    #button that graphs the calibration
    ct.plotCalibrationCurve(raw, PPM)
    graphCalibrationButton.config(text="Calibration Graphed :D")






"""Main loop"""

#Initialize the gui
root = tk.Tk()
root.title("Data Processing")
root.geometry("500x500")
#Add one button for the user to select the rawData file


rawDataButton = tk.Button(root, text="Select Raw Data File", command=lambda: SelectRawData())
rawDataButton.pack()

#Add one button for the user to select the dilutionTable file
dilutionTableButton = tk.Button(root, text="Select Dilution Table File", command=lambda: SelectDilutionTable())
dilutionTableButton.pack()


#Add a button to start the data processing
processDataButton = tk.Button(root, text="Process Data", command=lambda: processData())
processDataButton.pack()

#Button that asks for a directory to save the data to, and export the three tbales to csv files in that directory
exportDataButton = tk.Button(root, text="Export Data", command=lambda: exportToCSV(table1, table2, table3))
exportDataButton.pack()

#Add a button to select the ppm table for calibration
PPMTableForCalibrationButton = tk.Button(root, text="Select PPM Table For Calibration", command=lambda: SelectPPMTableForCalibration())
PPMTableForCalibrationButton.pack()

#Add a button to graph the calibration
graphCalibrationButton = tk.Button(root, text="Graph Calibration", command=lambda: graphCalibration(rawData, PPMTableForCalibration))
graphCalibrationButton.pack()




root.mainloop()





