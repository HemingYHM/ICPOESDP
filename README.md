# ICPOES Data Processing Tool with Calibration Curve plotter
 This is a data processing app that processes raw data from the ICPOES device and allows the user to plot calibration curves for the elements of interest. The app is written in Python and belong to SALT lab at UC Berkeley. 

 ### Installation
 The App is writting in Python 3.7 and uses the following libraries: 
 - Pandas
 - Numpy
 - Matplotlib

 ### In Progress
 - Shell Script thta initializes an virtual environment and installs the libraries for the user.
 - Dedicated GUI for the Calibration Curve plotter?

To install the libraries, run the following command in the terminal, contact hemingy@berkeley.edu if you run into any issues:
```
pip install pandas
pip install numpy
pip install matplotlib
```


### How to use the app
To run the Data Processing tool, type the following commands into terminal 

```
cd [The directory that you downloaded the app]
python3 nonOfficialdp.py
```

To run the calibrationTool
```
cd [The directory that you downloaded the app]
python3 calibrationTool.py
```
Make sure in the GUI that you have selected the Raw Data Table as well as the output PPM table for the Calibration curve in order for it to work correctly.

***Note:*** 
The Calibration curve will plot all elements that are UNIQUE in the table, so make sure that you read the title of the graph and make sure that it is correct. 
 
*** Close the graph to proceed to next element. ***

### Links
- [SALT Lab](https://salt.engin.berkeley.edu/)
- [Documentation](https://salt.nuc.berkeley.edu/) (Ony accessible to SALT lab members)