import os

chromDir = os.getcwd() + '\\Chromatogram_CSVs\\'
heatDir = os.getcwd() + '\\HeatMap_CSVs\\'
trendDir = os.getcwd() + '\\Trend_CSVs\\'


dirList = [chromDir, heatDir, trendDir]

#chromCheck = os.path.isdir(chromDir)
#chromCheck = os.path.isdir(chromDir)
#chromCheck = os.path.isdir(chromDir)

for dir in dirList:
	# If folder doesn't exist, then create it.
	dirCheck = os.path.isdir(dir)
	if not dirCheck:
    		os.makedirs(dir)
    		print("Created folder : ", dir)
	else:
		continue