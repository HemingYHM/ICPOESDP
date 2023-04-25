import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#Plotting the calibration cuvre for each analyte
def plotCalibrationCurve(rawData):
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

    #Graph Name: Analyte Name Calibration Curve 
    #X axis: Sample ID
    #Y axis: Int (Corr)
    #Line of best fit: y = mx + b
    
    #get the unique analyte names
    analyteNames = tempTable['Analyte Name'].unique()
    #parse sample ID into numbers, and remove the ppm at the end
    tempTable['Sample ID'] = tempTable['Sample ID'].str.replace('ppm', '')
    tempTable['Sample ID'] = tempTable['Sample ID'].astype(float)
    #loop through each analyte name

    for analyte in analyteNames:
        #get the data for the current analyte
        currentAnalyteData = tempTable[tempTable['Analyte Name'] == analyte]
        #get the x and y values
        x = currentAnalyteData['Sample ID']
        y = currentAnalyteData['Int (Corr)']
        #plot the data points
        plt.scatter(x, y, label = analyte)
        #plot the line of best fit
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m*x + b, label = analyte + ' Line of Best Fit')
        #set the title
        plt.title(analyte + ' Calibration Curve')
        #set the x and y labels
        plt.xlabel('Sample ID')
        plt.ylabel('Intensity')
        #show the legend
        plt.legend()
        #show the graph
        plt.show()




plotCalibrationCurve('aprNew.csv')