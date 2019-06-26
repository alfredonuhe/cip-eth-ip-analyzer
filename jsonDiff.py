# Code to detect differences between JSON files

import sys, os, time
import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from progressBar import *
from DataImporter import DataImporter

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

def main():
	startTime = time.time()
	dfList = []	
	jsonPath = [0, "_source", "layers", "cipcls", "Command Specific Data", "cip.data"]
	startLines = None
	paths = None
	numInstances = None
	
	if (len(sys.argv) < 4):
			print("Error, two file paths must be entered using '-f'.")
			exit()

	for i in range(1, len(sys.argv)):
		if(sys.argv[i][0] == "-"):
			if (sys.argv[i] == "-f"):
				paths = [sys.argv[i + 1], sys.argv[i + 2]]
			elif (sys.argv[i] == "-s"):
				startLines = [int(sys.argv[i + 1]), int(sys.argv[i + 2])]
				print()
			elif (sys.argv[i] == "-n"):
				numInstances = int(sys.argv[i + 1])
			else:
				print("Error, invalid argument '", sys.argv[i], "'.")
				exit()
		else:
			continue
	
	if (paths == None): print("Error, file paths must be set with the argument '-f'.")
	if (startLines == None): startLines = [0,0]
	if (numInstances == None): numInstances = 100
	
	for path in paths:
		if not os.access(path, os.R_OK):
			print("Error, the file path ", path, " isn't accessible.")
			exit()

		print("Opening JSON file at path " + path + " ...\n")		
			
		# Stack all network payloads from JSON file into a pandas
		# Dataframe.
		maxPayloads = numInstances + max(startLines) + 1

		di = DataImporter(path, jsonPath, 4, maxPayloads)
		di.init()
		dfList.append(di.df)

	for i in range(0, len(dfList)): dfList[i] = dfList[i].loc[startLines[i]:(startLines[i] - 1) + numInstances, :].reset_index(drop = True)
	
	dfList = orderDfList(dfList)
	indexS = 0
	indexB = 0
	dfInd = [indexS, indexB]
	
	while (dfInd[0] < dfList[0].shape[0] and dfInd[1] < dfList[1].shape[0]):
		while (True):
			command = input("\nPress 'Enter' to coninue to row (" + str(dfInd[0]) + ", " + str(dfInd[1]) + "), 'q' to exit ...")
			if (command == 'q'): exit()
			elif (command == 'm'):
				n = input("Enter the DataFrame number (0 or 1):")
				index = input("Enter new index for DataFrame " + str(n) + ":")
				if (n == '0'): dfInd[0] = int(index)
				elif (n == '1'): dfInd[1] = int(index)
				else:
					print("Wrong DataFrame number.")
			else: break
		
		print(dfInd)
		
		for n in range(0, len(dfList)):
			for j in range(0, dfList[0].shape[1]):
				if (dfList[0].loc[dfInd[0], j] != None or dfList[1].loc[dfInd[1], j] != None):	
					if (j > 0): print(":", end = "")
					if (dfList[n].loc[dfInd[n], j] != None):
						if (dfList[0].loc[dfInd[0], j] != dfList[1].loc[dfInd[1], j]):
							sys.stdout.write(RED)
						print(hex(int(dfList[n].loc[dfInd[n], j]))[-1], end = "")
					elif (dfList[n].loc[dfInd[n], j] == None and dfList[(n + 1) % 2].loc[dfInd[(n + 1) % 2], j] != None):
						sys.stdout.write(RED)
						print(".", end = "")
					sys.stdout.write(RESET)
			print("\n")
		dfInd[0] += 1
		dfInd[1] += 1

def orderDfList(dfList):
	bigDF = None
	smallDF = None

	if (dfList[0].shape[1] < dfList[1].shape[1]):
		smallDF = dfList[0]
		bigDF = dfList[1]
	elif (dfList[0].shape[1] > dfList[1].shape[1]):
		smallDF = dfList[1]
		bigDF = dfList[0]
	else:
		return dfList

	return [smallDF, bigDF]

def clearConsoleLines(n):
	if(n < 0):
		print("Error, it is not possible to clear '", n, "' lines")	
	print('\033[F' * n, end = "")
	print(" " * n * 100, end = "")
	print('\033[F' * n, end = "")

# Main function
if __name__ == "__main__":
    main()