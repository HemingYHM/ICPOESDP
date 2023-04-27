"""Data Processing Utility Functions"""

import matplotlib.pyplot as plt
import pandas as pd
import warnings
import numpy as np
import os

"#disable warnings"
warnings.filterwarnings('ignore')

#read raw data from file and return pandas table
def readData(fileName):
    data = pd.read_csv(fileName)
    return data

#Using the raw data table , return a table with the average of the 3 replicates and standard deviation
def getAverageAndStd(rawData, dilutionTable):
    #Sicnce sample names are in format of 10B1[01]01A20221108, we only keep samples with lengh greater than 10 and start with 10
    tempdata = rawData
    tempdata = tempdata[tempdata['Sample ID'].str.len() > 10]
    tempdata = tempdata[tempdata['Sample ID'].str.startswith('10')]
    
    #Create a new table with only the values needed: Sample ID, Analyte Name, Conc (Calib)1, Conc (Calib)2, Conc (Calib)3. As well as the given RSDs
    tempTable = tempdata[['Sample ID', 'Analyte Name', 'Conc (Calib)1', 'Conc (Calib)2', 'Conc (Calib)3', 'RSD (Corr Int)', 'RSD (Conc)']]

    #parse numerical columns to float
    tempTable['Conc (Calib)1'] = tempTable['Conc (Calib)1'].astype(float)
    tempTable['Conc (Calib)2'] = tempTable['Conc (Calib)2'].astype(float)
    tempTable['Conc (Calib)3'] = tempTable['Conc (Calib)3'].astype(float)
    tempTable['RSD (Corr Int)'] = tempTable['RSD (Corr Int)'].astype(float)
    tempTable['RSD (Conc)'] = tempTable['RSD (Conc)'].astype(float)

    #Calculate the average of the 3 replicates by brute force
    tempTable['Calculated Average'] = tempTable[['Conc (Calib)1', 'Conc (Calib)2', 'Conc (Calib)3']].mean(axis=1)
    #Calculate the standard deviation of the 3 replicates
    tempTable['Calcuated Std Dev'] = tempTable[['Conc (Calib)1', 'Conc (Calib)2', 'Conc (Calib)3']].std(axis=1)
    #Drop the 3 replicates
    tempTable = tempTable.drop(['Conc (Calib)1', 'Conc (Calib)2', 'Conc (Calib)3'], axis=1)

    #Convert Machine given RSD into standard deviation and add to the table
    tempTable['Machine Std Dev'] = tempTable['RSD (Conc)'] * tempTable['Calculated Average'] / 100

    #The volumn digestion is stored in dilutionTbale 
    #The mass of digestion is stored in dilutionTable
    for row in tempTable.itertuples():
        digestionVolumn = dilutionTable[dilutionTable['SA ID '] == row[1]]["volume digestion (ml)"].values[0].astype(float)
        mass = dilutionTable[dilutionTable['SA ID '] == row[1]]["mass sample (g)"].values[0].astype(float)
        tempTable.loc[row[0], 'Digestion Volumn'] = digestionVolumn
        tempTable.loc[row[0], 'Mass'] = mass


    #Error Column
    #Error = srqt((Volumn of Digestion * mass of digestion * sd of current)**2 + (Volumn of D * Mass of D * 1.5)**2 + (Volumn of D * Mass of D * 5)**2)
    tempTable['Error'] = np.sqrt((tempTable['Digestion Volumn'] * tempTable['Mass'] * tempTable['Calcuated Std Dev'])**2 + (tempTable['Digestion Volumn'] * tempTable['Mass'] * 1.5)**2 + (tempTable['Digestion Volumn'] * tempTable['Mass'] * 5)**2)
    return tempTable


#Table with only the blank samples
def getBlankTable(avgAndStdDev):
    #Create a new table with only the values needed: Sample ID, Analyte Name, Conc (Calib)1, Conc (Calib)2, Conc (Calib)3. As well as the given RSDs
    tempTable = avgAndStdDev.copy()
    #only keep rows that start with 10B
    tempTable = tempTable[tempTable['Sample ID'].str.startswith('10B')]
    

    return tempTable




#Calculate the PPM using dilution table and the average and standard deviation table
def calculatePPM(blankTable, dilutionTable, avgAndStdDev):
    #loop through rows of avgAndStdDev
    for index, row in avgAndStdDev.iterrows():
        #get the sample ID
        sampleID = row['Sample ID']
        #skip blank samples
        if sampleID.startswith('10B'):
            continue
        #get the analyte name
        analyteName = row['Analyte Name']
        digestionVolumn = dilutionTable[dilutionTable['SA ID '] == sampleID]["volume digestion (ml)"].values[0].astype(float)
        mass = dilutionTable[dilutionTable['SA ID '] == sampleID]["mass sample (g)"].values[0].astype(float)
        dilutionfactor = dilutionTable[dilutionTable['SA ID '] == sampleID]["dilution factor"].values[0].astype(float)
        concentratedInBlank = blankTable[blankTable['Analyte Name'] == analyteName]["Calculated Average"].values[0].astype(float)
        concentrated = row['Calculated Average']

        calculatedDilutionConstant = (digestionVolumn/mass) * dilutionfactor
        if concentratedInBlank > 0:
            finalPPM = (concentrated - concentratedInBlank) * calculatedDilutionConstant
        else:
            finalPPM = concentrated * calculatedDilutionConstant
        if finalPPM > 0:    
            avgAndStdDev.loc[index, 'Final PPM'] = finalPPM

    #remove blanks 
    avgAndStdDev = avgAndStdDev[avgAndStdDev['Sample ID'].str.startswith('10B') == False]
    #remove empty ppm 
    avgAndStdDev = avgAndStdDev[avgAndStdDev['Final PPM'].isnull() == False]
    return avgAndStdDev



#Export Everything to csv Files
def exportToCSV(avgAndStdDev, blankTable, ppmTable):
    #make a new folder in current directory and export all tables to csv files
    currentDirectory = os.getcwd()
    newDirectory = currentDirectory + "/output"
    #export the three input tables to csv files in new directory
    if not os.path.exists(newDirectory):
        mkdirCommand = "mkdir " + newDirectory
        os.system(mkdirCommand)

    #if the column is empty in avg or ppm table, fill it with 0 

    avgAndStdDev.to_csv(newDirectory + "/avgAndStdDev.csv")
    blankTable.to_csv(newDirectory + "/blankTable.csv")
    ppmTable.to_csv(newDirectory + "/ppmTable.csv")













def workupData(rawData, dilutionTable):
    """returns the average and standard deviation table, blank table, and ppm table in a triple"""

    rawData = readData(rawData)
    dilutionTable = readData(dilutionTable)
    avgAndStdDev = getAverageAndStd(rawData, dilutionTable)
    blankTable = getBlankTable(avgAndStdDev)
    ppmTable = calculatePPM(blankTable, dilutionTable, avgAndStdDev)

    #fill empty columns with 0 for avgAndStdDev and ppmTable
    avgAndStdDev = avgAndStdDev.fillna(0)
    ppmTable = ppmTable.fillna(0)
    
    return avgAndStdDev, blankTable, ppmTable