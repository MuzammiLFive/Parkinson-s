# PD
Simple GUI Application to Detect Parkinson's Disease using Adaptive Boosting algorithm.

Tools Used:
Python
TKinter - GUI in python

The Application is divided into 2 files

1) algorithm.py:
                This file is run first. It pre-processes the dataset and trains AdaBoost algorithm on the data.
                The model is then saved to the disk using Pickle.
2) Interface.py:
                An interface is created by this file that accepts new patient data. The interface accepts csv and excel file only.
                The model saved to the disk is accessed and used to classify the new data as Diagnosed or not.
