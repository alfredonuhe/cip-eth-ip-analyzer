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

def main():
	
	# Use tkinter librariy to be able to plot using a GUI.
	mpl.use("TkAgg")

	# File path to JSON file
	path = os.path.abspath('./Process2PCData/Process2PC.json')

	print("Opening JSON file at path " + path + "...\n")

	# Open JSON file containing network data sample.
	with open(path) as f:
		# Load sample to Python List object
		d = json.load(f)

		# Set variables needed for later.		
		length = len(d[0]["_source"]["layers"]["cipcls"]["Command Specific Data"]["cip.data"].split(":"))
		narray = np.zeros(length)
		
		print("Storing JSON file data in a pandas DataFrame...")

		# Extract from the JSON file the propietary protocol payload for 
		# each packet, and add it to a data matrix.
		for i in range(0, len(d)):
			sAux = d[i]["_source"]["layers"]["cipcls"]["Command Specific Data"]["cip.data"]
			sAux = sAux.split(":")
			sAux = hexToIntList(sAux)	
			narray = np.vstack((narray, sAux))
			# Printing progress bar for data 
			printProgressBar (i, len(d) - 1, 'Progress', 'Complete')

		# Remove the first row of zeros and store the matrix in a DataFrame.
		narray = narray[1:]
		df = pd.DataFrame(narray)
		
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
		
		print("Graphs stored at " + os.path.abspath('./Plots') + ".")

# Function to transform list with hex values into integer values.
def hexToIntList(hexList):
	for j in range(0, len(hexList)):
		hexList[j] = int(hexList[j], 16)
	
	return hexList
		
# Main function
if __name__ == "__main__":
    main()

# print(json.dumps(d[0]["_source"]["layers"]["cipcls"]["Command Specific Data"]["cip.data"], sort_keys=True, indent=4))
