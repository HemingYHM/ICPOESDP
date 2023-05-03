"""Data Processing Utility Functions"""

import matplotlib.pyplot as plt
import pandas as pd
import warnings
import numpy as np
import os
import math

"#disable warnings"
warnings.filterwarnings('ignore')

#read raw data from file and return pandas table
def readData(fileName):
    """Reads data from a csv file and returns a pandas table"""
    data = pd.read_csv(fileName)
    return data

#Using the raw data table , return a table with the average of the 3 replicates and standard deviation
def getAverageAndStd(rawData, dilutionTable):
    """Returns a table with the average of the 3 replicates and standard deviation, with some extra information regarding the sample
    such as error, calculated error, and sample intensity
    """
    #Sicnce sample names are in format of 10B1[01]01A20221108, we only keep samples with lengh greater than 10 and start with 10
    tempdata = rawData
    tempdata = tempdata[tempdata['Sample ID'].str.len() > 10]
    tempdata = tempdata[tempdata['Sample ID'].str.startswith('10')]
    
    #Create a new table with only the values needed: Sample ID, Analyte Name, Conc (Calib)1, Conc (Calib)2, Conc (Calib)3. As well as the given RSDs
    tempTable = tempdata[['Sample ID', 'Analyte Name', 'Conc (Calib)1', 'Conc (Calib)2', 'Conc (Calib)3', 'RSD (Corr Int)', 'RSD (Conc)', 'Int (Corr)', 'Conc (Calib)']]

    #parse numerical columns to float
    tempTable['Conc (Calib)1'] = tempTable['Conc (Calib)1'].astype(float)
    tempTable['Conc (Calib)2'] = tempTable['Conc (Calib)2'].astype(float)
    tempTable['Conc (Calib)3'] = tempTable['Conc (Calib)3'].astype(float)
    tempTable['RSD (Corr Int)'] = tempTable['RSD (Corr Int)'].astype(float)
    tempTable['RSD (Conc)'] = tempTable['RSD (Conc)'].astype(float)
    tempTable['Int (Corr)'] = tempTable['Int (Corr)'].astype(float)
    tempTable['Conc (Calib)'] = tempTable['Conc (Calib)'].astype(float)

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


    #Calculate the error of the sample
    #Calculated Error = sqrt( (B * D/C * deltaA)^2 + (A * D/C * deltaB)^2 + (- (D/C^2 *A *B) * deltaC)^2)
    #A = Concentration of the analyte in the sample, B = Digestion Volumn, C = Sample Mass, D = dilutionFactor 
    #DeltaA = Machine given RSD, DeltaB = 2.7, DeltaC = 1.5, DeltaD = 0

    #Calculate the error of the sample

    
    tempTable['XError'] = tempTable["RSD (Conc)"] * tempTable['Conc (Calib)'] / 100
    tempTable['XError'] = tempTable['XError'].abs()

    
    #Y error is the machine given RSD * Int (Corr)
    tempTable['YError'] = tempTable['RSD (Corr Int)'] * tempTable['Int (Corr)'] / 100
    return tempTable


#Table with only the blank samples
def getBlankTable(avgAndStdDev):
    """Returns a table with only the blank samples, this method is implemented to make sure that 
    we are captuing the correct blank samples"""
    #Create a new table with only the values needed: Sample ID, Analyte Name, Conc (Calib)1, Conc (Calib)2, Conc (Calib)3. As well as the given RSDs
    tempTable = avgAndStdDev.copy()
    #only keep rows that start with 10B
    tempTable = tempTable[tempTable['Sample ID'].str.startswith('10B')]
    

    return tempTable




#Calculate the PPM using dilution table and the average and standard deviation table
def calculatePPM(blankTable, dilutionTable, avgAndStdDev):
    """Calculates the PPM of each sample using the blank table, dilution table, and the average and standard deviation table 
    using the fomula that is given in the ICPOES data workbook, detailed in the report and documentation
    """
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
        rsd = row['RSD (Conc)']


        calculatedDilutionConstant = (digestionVolumn/mass) * dilutionfactor
        if concentratedInBlank > 0:
            
            finalPPM = (concentrated - concentratedInBlank) * calculatedDilutionConstant
            concentrated = concentrated - concentratedInBlank
        else:
            finalPPM = concentrated * calculatedDilutionConstant
        if finalPPM > 0:    
            avgAndStdDev.loc[index, 'Final PPM'] = finalPPM

        delA = rsd * concentrated / 100
        delB = 2.8
        delC = 0.0015
        delD = 0

        A = concentrated
        B = digestionVolumn
        C = mass
        D = dilutionfactor

        calcError = math.sqrt( (B * D/C * delA)**2  + (A * D/C * delB)**2 + (- (D/C**2 *A *B) * delC)**2 + (A*B/C*delD)**2)
    

        avgAndStdDev.loc[index, 'Calculated Error'] = calcError


    #remove blanks 
    avgAndStdDev = avgAndStdDev[avgAndStdDev['Sample ID'].str.startswith('10B') == False]
    #remove empty ppm 
    avgAndStdDev = avgAndStdDev[avgAndStdDev['Final PPM'].isnull() == False]

    #only keep the SA ID, analyte name, and final ppm
    ppmTable = avgAndStdDev[['Sample ID', 'Analyte Name', 'Final PPM', 'Calculated Error']]
    
    #Loop thorugh the ppm table and add the calculated Error accordingly

    return ppmTable



#Export Everything to csv Files
def exportToCSV(avgAndStdDev, blankTable, ppmTable):
    """Exports the average and standard deviation table, blank table, and ppm table to csv files in a new folder called output"""

    #make a new folder in current directory and export all tables to csv files
    currentDirectory = os.getcwd()
    newDirectory = currentDirectory + "/output"
    #export the three input tables to csv files in new directory
    if not os.path.exists(newDirectory):
        mkdirCommand = "mkdir " + newDirectory
        os.system(mkdirCommand)

    #if the column is empty in avg or ppm table, fill it with 0 

    #Add the Calculated Error from the ppm table to the avgAndStdDev table, only for the rows with same sample ID and analyte name
    for index, row in ppmTable.iterrows():
        sampleID = row['Sample ID']
        analyteName = row['Analyte Name']
        ppm = row['Final PPM']
        error = row['Calculated Error']
        avgAndStdDev.loc[(avgAndStdDev['Sample ID'] == sampleID) & (avgAndStdDev['Analyte Name'] == analyteName), 'Final PPM'] = ppm
        avgAndStdDev.loc[(avgAndStdDev['Sample ID'] == sampleID) & (avgAndStdDev['Analyte Name'] == analyteName), 'Calculated Error'] = error


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