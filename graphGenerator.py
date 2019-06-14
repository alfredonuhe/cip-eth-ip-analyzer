# Code to detect patterns on network packet communication propietary protocols.
# The code reads the network data sample from a JSO file and plots the value 
# of each byte over time.

import sys, os
import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from progressBar import *
from dataExtractor import *

def main():
	
	# Use tkinter librariy to be able to plot using a GUI.
	mpl.use("TkAgg")

	# File path to JSON file
	path = os.path.abspath('./Process2PCData/Process2PC.json')
	
	# JSON structure path to desired information. 
	infoPath = [0, "_source", "layers", "cipcls", "Command Specific Data", "cip.data"]

	print("Opening JSON file at path " + path + " ... ", end = "")

	# Open JSON file containing network data sample.
	with open(path) as f:
		# Load sample to Python List object
		d = json.load(f)
		print("Done.\n")		
		
		# Stack all network payloads from JSON file into a pandas
		# Dataframe.
		print("Storing JSON file data in a pandas DataFrame ... ")
		df = gatherJSONData(path, infoPath)
		
		print("Calculating byte graphs...")

		# Plot the values of each byte over time into separate figures.
		for i in range(0, len(df.loc[0,:])):
			plt.clf()
			plt.plot(df.index[:51], df.loc[:50,i], label='Byte #' + str(i))
			plt.xlabel('Time')
			plt.ylabel('Value')
			plt.title("Behaviour of byte #" + str(i))
			plt.savefig("./Plots/BehavBite" + str(i) + ".png")
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
