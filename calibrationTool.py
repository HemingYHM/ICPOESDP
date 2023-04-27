import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#TEST
#Plotting the calibration cuvre for each analyte

deltaC = 1.5
deltaD = 5

def plotCalibrationCurve(rawData, ppmTable):
    """Reads in the raw data, and first constructs the calibration table

    Calibration Table, this would be only consisted of the Sample ID that are numbers i.e 0, 25, 50, 100, since those are 
    used to plot the calibration cuvres

    The Sample ID would be used as the X axis, and the Intensity would be used as the Y axis of each data point

    Then, create a line of best fit for each analyte, and plot the line of best fit with the data points
    
    """

    rawData = pd.read_csv(rawData)
    #Create a new table with only the values needed: Sample ID, Analyte Name, Int (Corr)
    tempTable = rawData[['Sample ID', 'Analyte Name', 'Int (Corr)']]
    #one edge case: when sample ID's name is Calib Blank 1, change it to 0ppm
    tempTable.loc[tempTable['Sample ID'] == 'Calib Blank 1', 'Sample ID'] = '0ppm'
    #Only keep sample id that ends with PPM 
    tempTable = tempTable[tempTable['Sample ID'].str.endswith('ppm')]
    #if there are duplicate Sample ID, and analyte name keep the latter one
    tempTable = tempTable.drop_duplicates(subset=['Sample ID', 'Analyte Name'], keep='last')
    ppmError = pd.read_csv(ppmTable)
    #Graph Name: Analyte Name Calibration Curve 
    #X axis: Sample ID
    #Y axis: Int (Corr)
    #Line of best fit: y = mx + b
    
    #get the unique analyte names
    analyteNames = tempTable['Analyte Name'].unique()
    #parse sample ID into numbers, and remove the ppm at the end
    tempTable['Sample ID'] = tempTable['Sample ID'].str.replace('ppm', '')
    tempTable['Sample ID'] = tempTable['Sample ID'].astype(float)

    print(ppmError)
    #loop through each analyte name

    for analyte in analyteNames:
        #get the data for the current analyte
        currentAnalyteData = tempTable[tempTable['Analyte Name'] == analyte]
        #get the x and y values
        xfit = currentAnalyteData['Sample ID']
        yfit = currentAnalyteData['Int (Corr)']

        #plot the data points
        #plot the line of best fit
        m, b = np.polyfit(xfit, yfit, 1)
        plt.xlabel('PPM')
        plt.ylabel('Intensity')

        
        #Plot the data points from PPM table that has same analyte name, x being ppm y being 0
        ppmErrorData = ppmError[ppmError['Analyte Name'] == analyte]
        ID = ppmErrorData['Sample ID']
        X = ppmErrorData['Final PPM']
        #Y is the line of best first 
        Y = m*X + b
        error = ppmErrorData['Error']
        #plot the data points
        plt.errorbar(X, Y, yerr = error, fmt = 'o', label = analyte + ' Data Points')
        #plot the line of best fit

        #Graph Name
        plt.title(analyte + ' Calibration Curve')
        #X axis
        plt.xlabel('PPM')
        #Y axis
        plt.ylabel('Intensity')
        plt.plot(X, Y, label = analyte + ' Line of Best Fit')
        plt.legend()
        plt.show()



    #Error Propagation






plotCalibrationCurve('aprNew.csv', 'ppmTable.csv')
