#write a program with a gui that asks for two user imputs, one named Rawdata, one named dilution table. 
#Then it will save it to two variables, and apply dpUtil functions to it.

import tkinter as tk
from tkinter import filedialog
from tkinter import *
import pandas as pd
import dpUtil as dp


def SelectRawData():
    global rawData
    rawData = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    rawDataButton.config(text = str(rawData))


def SelectDilutionTable():
    global dilutionTable
    dilutionTable = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    dilutionTableButton.config(text = str(dilutionTable))

def processData():
    #button that processes the data
    global table1, table2, table3
    table1, table2, table3 = dp.workupData(rawData, dilutionTable)
    processDataButton.config(text="Data Processed :D")

def exportToCSV(table1, table2, table3):
    #button that asks for a directory to save the data to, and export the three tbales to csv files in that directory
    directory = filedialog.askdirectory()
    table1.to_csv(directory + "/avgAndStdDev.csv")
    table2.to_csv(directory + "/blankTable.csv")
    table3.to_csv(directory + "/ppmTable.csv")
    exportDataButton.config(text="Data Exported :D")








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

root.mainloop()





