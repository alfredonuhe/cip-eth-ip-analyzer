# Code to detect patterns on network packet communication propietary protocols.
# The code reads the network data sample from a JSO file and plots the value 
# of each byte over time.

import sys, os
from subprocess import run
import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from progressBar import *
from DataImporter import DataImporter

def main():
	
	# Use tkinter librariy to be able to plot using a GUI.
	mpl.use("TkAgg")

	# File path to JSON file
	path = os.path.abspath('./Process2PCData/Process2PC.json')
	
	# JSON structure path to desired information. 
	infoPath = [0, "_source", "layers", "cipcls", "Command Specific Data", "cip.data"]

	# Bit length to represent the binary data in the 
	# pandas DataFrame
	bitLength = 4

	# Maximum number of payloads to import
	maxPayloads = 50
	
	# Stack all network payloads from JSON file into a pandas
	# Dataframe.
	print("Opening JSON file at path ", path, " ...\n")
	di = DataImporter(path, infoPath, bitLength, maxPayloads)
	di.init()
	df = di.df
	
	print("Calculating byte graphs...")
	
	# Reset Plots directory for new graphs
	if os.path.isdir("./Plots"):
		run(["rm", "-rf", "./Plots"])

	run(["mkdir", "./Plots"])

	# Plot the values of each byte over time into separate figures.
	for i in range(0, len(df.loc[0,:])):
		plt.clf()
		plt.plot(df.index, df.loc[:,i], label='Byte #' + str(i))
		plt.xlabel('Time')
		plt.ylabel('Value')
		plt.title("Behaviour #" + str(i))
		plt.savefig("./Plots/BehavBit" + str(i) + ".png")
		printProgressBar (i, len(df.loc[0,:]) - 1, 'Progress', 'Complete')
	
	print("Graphs succesfully stored at " + os.path.abspath('./Plots') + ".")

# Function to transform list with hex values into integer values.
def hexToIntList(hexList):
	for j in range(0, len(hexList)):
		hexList[j] = int(hexList[j], 16)
	
	return hexList
		
# Main function
if __name__ == "__main__":
    main()
