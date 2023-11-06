import pandas as pd
from statistics import mean
import math
#from decimal import Decimal, ROUND_HALF_UP

# Method for Rounding Values at 0.05 UP
def normal_round(n):
	if n*100 - math.floor(n*100) <= 0.5:
		x = math.ceil(n*100)
		y = x/100
		return y
	else:
    		return round(n,2)


# Create Sorted List of all RT Values
def RTList(fullDict):
	RTList = fullDict["RT [min]"].values.tolist()
	staticRTList = RTList.copy()
	RTList = list(dict.fromkeys(RTList))
	RTList.sort()
	return RTList, staticRTList	

# Create Sorted List of all RRT Values
def RRTList(fullDict):
	RRTList = fullDict["RRT"].values.tolist()
	staticRRTList = RRTList.copy()
	RRTList = list(dict.fromkeys(RRTList))
	RRTList.sort()
	return RRTList, staticRRTList	

# DETERMINE THE MEAN VALUE OF RRT 1.00 IN MIN 
def rrtOneFinder(fullDict):
	rtONEList = fullDict.query("RRT==1")["RT [min]"]
	if len(rtONEList) == 0:
		print("RRTs not provided, RRT 1.00 will be calulated as the mean of all RTs given:")
		rtSum = fullDict["RT [min]"].sum()
		#print(rtSum)
		rtOneAVG = rtSum/len(fullDict)
		print("RRT 1.00 calulated as: {:.3f} min".format(rtOneAVG))
	else:
		rtOneAVG = rtONEList.sum()/len(rtONEList)
		print("RRT 1.00 given as: {:.3f} min".format(rtOneAVG))
	
	return rtOneAVG

# RECALCULATE RT VALUES
def calRTValues(rtOneAVG, RRTList, x):
	reCalcdRTs = []
	for rrt in RRTList:
		reCalcdRTs.append(round(float(rrt)*rtOneAVG, x))

	return reCalcdRTs

# SET RRTs FROM MEAN RRT 1.00
def normaliseRRTs(fullDict,rtOneAVG):
	unusedSortedValue,rtIndex = RTList(fullDict) #fullDict["RT [min]"].values.tolist()
	rawharmanisedRRTs = list(map(lambda x: x/rtOneAVG, rtIndex))
	harmanisedRRTs = [ '%.3f' % elem for elem in rawharmanisedRRTs ]
	
	print(harmanisedRRTs)
	
	# Drop that column
	fullDict.drop(["RRT"], axis = 1, inplace = True)

	# Put whatever series you want in its place
	fullDict["RRT"] = harmanisedRRTs


# FIND AND SORT ALL THE RRT VALUES, COMPUND IDs AND SAMPLE NAMES
def sortNamedCMPDs(fullDict):

	rrtIndex, rrtList = RTList(fullDict)
	cmpnameIndex = fullDict["Compound Name"].dropna().values.tolist()
	cmpnameList = cmpnameIndex.copy()
	cmpnameIndex = list(dict.fromkeys(cmpnameIndex))
	#cmpdfIndex = []
	meanRRTbyCMPD = []
	cmpdKVDict = {}
	twodpcmpdKVDict = {}

	for cmpdValue in cmpnameIndex:
		foundRRTvalue = fullDict.loc[(fullDict['Compound Name'] == cmpdValue), 'RRT'].dropna()
		matchingRRTList = []
		twodpmatchingRRTList = []
		for matchingRRT in foundRRTvalue:
			matchingRRTList.append(float(matchingRRT))
			twodpmatchingRRTList.append(round(float(matchingRRT),2))
		cmpdKVDict[cmpdValue] = matchingRRTList
		twodpcmpdKVDict[cmpdValue] = twodpmatchingRRTList
	print('\n')
	print(cmpdKVDict)
	print('\n')
	meanRRTcmpdDict = {}
	for key in cmpdKVDict:
		meanRRTbyCMPD = mean(cmpdKVDict[key])
		meanRRTcmpdDict[key] = meanRRTbyCMPD
	res_key, res_val = min(meanRRTcmpdDict.items(), key=lambda x: abs(1.000 - x[1]))
	if res_val < 1.1 and res_val > 0.9:
		meanRRTcmpdDict[res_key] = 1.000
		RRToneCheck = True
		RRToneKey = res_key
	else:
		RRToneCheck = False
		RRToneKey = ' '

	return cmpdKVDict, RRToneCheck, RRToneKey, meanRRTcmpdDict, twodpcmpdKVDict

# GET LIST OF CMPD NAMES OF RIGHT LIST LENGTH FOR RRTs
def getCMPDListforRRT(RRTList, cmpdKVDict):
	inLineCMPDList = []
	for RRTvalue in RRTList:
		key_with_value = [k for k, v in cmpdKVDict.items() if float(RRTvalue) in v]
		if len(key_with_value) == 1:
			inLineCMPDList.append(key_with_value[0])
		elif len(key_with_value) > 1:
			concatKeys = key_with_value.join(' + ')
			inLineCMPDList.append(concatKeys)
		else:
			inLineCMPDList.append(' ')

	return inLineCMPDList


# CONVERT AREA TO %AREA
def percentAreaCal(trendedDF, newTopRows):
	santyDF = trendedDF
	percentAreaDF = newTopRows
	blankAreaDF = pd.DataFrame()
	print('\n\n')
	for column in santyDF.columns[:-1]:
		blankAreaDF[column] = round(santyDF[column][3:].astype(float) / santyDF['Sum'][3:].astype(float) * 100, 2)
	for index,row in blankAreaDF.iterrows():
		percentAreaDF.loc[index] = row
			
	percentAreaDF.rename(index={0:'Compound'},inplace=True)
	percentAreaDF = percentAreaDF.drop(['Sum'], axis=1)
	percentAreaDF.iloc[0], percentAreaDF.iloc[1] =  percentAreaDF.iloc[1].copy(), percentAreaDF.iloc[0].copy()
	percentAreaDF = percentAreaDF.rename(index={'RRT': 'temp'})
	percentAreaDF = percentAreaDF.rename(index={'RT': 'RRT'})
	percentAreaDF = percentAreaDF.rename(index={'temp': 'RT'})
	prettyperAreaDF = percentAreaDF.replace(0, '-')
	print(prettyperAreaDF)
	return percentAreaDF, prettyperAreaDF

# SIMPLIFY RRTs DOWN AS MUCH AS IS REASONABLE
def simplifyRRTs(namelessPeaks):
	dumbWorkAround = 0
	skipCheck = 0
	groupedAvgs = []
	for item in namelessPeaks:
		nextIndex = dumbWorkAround + 1
		if len(namelessPeaks) > nextIndex and skipCheck == 0:
			if float(namelessPeaks[nextIndex]) - float(item) < 0.02:
				mergeItem = (float(item) + float(namelessPeaks[nextIndex]))/2
				skipCheck = 1
			else:
				mergeItem = float(item)
				skipCheck = 0
		else:
			mergeItem = float(item)
			skipCheck = 0

		groupedAvgs.append(mergeItem)
		dumbWorkAround += 1

	print('\n')
	#print(groupedAvgs)
	formattedAvgs = []
	for AVG in groupedAvgs:
		formattedAvgs.append(normal_round(AVG))
	print('\n')
	#formattedAvgs = list(dict.fromkeys(formattedAvgs))
	print(formattedAvgs)
	return formattedAvgs