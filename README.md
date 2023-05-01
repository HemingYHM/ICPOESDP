# ICPOES Data Processing Tool with Calibration Curve plotter
 This is a data processing app that processes raw data from the ICPOES device and allows the user to plot calibration curves for the elements of interest. The app is written in Python and belong to SALT lab at UC Berkeley. 

 ### Installation
 The App is writting in Python 3.7 and uses the following libraries: 
 - Pandas
 - Numpy
 - Matplotlib
 ### How to set up virtual environment for ICPOESDP 
 1. We want to first: Initialize the virtual enviroment, please make sure you have python installed, ther version I use is 3.7
```
python3 -m venv ICPOESDP
```
or
```
python -m venv ICPOESDP
```
2. Activate the virtual environment
```
source ICPOESDP/bin/activate
```
3. Install all the dependencies using pip install
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
Make sure in the GUI that you have selected the Raw Data Table as well as the output PPM table for the Calibration curve in order for it to work correctly.

***Note:*** 
The Calibration curve will plot all elements that are UNIQUE in the table, so make sure that you read the title of the graph and make sure that it is correct. 
 

### Links
- [SALT Lab](https://salt.engin.berkeley.edu/)
- [Documentation]: IN PROGRESS