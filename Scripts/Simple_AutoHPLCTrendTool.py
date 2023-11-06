import matplotlib.pyplot as plt
import os
import pandas as pd
import warnings
import StyleTT
import customFunctions
from statistics import mean

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

wd = os.getcwd() + '\\Trend_CSVs\\'
print('Trending HPLC Integrals')

def trendHPLC(path,file):
	# SETUP DATABASE OF RESULTS FROM XLSX FILE
	sheetDict = {}
	fullName = path+file
	xlsx = pd.ExcelFile(fullName)
	fullDict = pd.concat(pd.read_excel(fullName, sheet_name=None), ignore_index=True)
	
	# DETERMINE THE MEAN VALUE OF RRT 1.00 IN MIN 
	rtOneAVG = customFunctions.rrtOneFinder(fullDict)

	# SET RRTs FROM MEAN RRT 1.00
	customFunctions.normaliseRRTs(fullDict,rtOneAVG)
	print('\n')
	print(fullDict)
	print('\n')

	# FIND AND SORT ALL THE RRT VALUES, COMPUND IDs AND SAMPLE NAMES
	cmpdKVDict, RRToneCheck, RRToneKey, meanRRTcmpdDict, twodpcmpdKVDict = customFunctions.sortNamedCMPDs(fullDict)

	# SEPERATE DATAFRAME VALUES INTO SAMPLE INJECTIONS AND BUILD NEW DATAFRAME
	RRTList, staticRRTList = customFunctions.RRTList(fullDict)
	reCalcdRTs = customFunctions.calRTValues(rtOneAVG, RRTList, 3)
	reCalcdRTs.append(' ')
	RTList, staticRTList = customFunctions.RTList(fullDict)
	inLineCMPDList = customFunctions.getCMPDListforRRT(RRTList, cmpdKVDict)
	inLineCMPDList.append(' ')
	print(inLineCMPDList)
	meanRRTListforCMPDs = []
	for RRTvalue in RRTList:
		key_with_value = [k for k, v in cmpdKVDict.items() if float(RRTvalue) in v]
		if len(key_with_value) == 1:
			meanRRTListforCMPDs.append(round(meanRRTcmpdDict[key_with_value[0]],3))
		else:
			meanRRTListforCMPDs.append(float(RRTvalue))
	meanRRTListforCMPDs.append('Sum')
	print(meanRRTListforCMPDs)
	RRTwithSum = RRTList.copy()
	RRTwithSum.append('Sum')
	sampleIndex = fullDict["Sample Name"].values.tolist()
	sampleIndex = list(dict.fromkeys(sampleIndex))
	trendedDF = pd.DataFrame(RRTwithSum)
	trendedDF['RT'] = reCalcdRTs
	trendedDF['RRT'] = meanRRTListforCMPDs
	trendedDF['Compound'] = inLineCMPDList
	counteri = 0
	for sampleName in sampleIndex:
		tempList = []
		sumList = []
		for rrtValue in RRTList:
			areadfValue = fullDict.loc[(fullDict['Sample Name'] == sampleName) & (fullDict["RRT"] == rrtValue), 'Area']
			areaValue = areadfValue.array
			if len(areaValue) > 0:
				tempList.append(areaValue[0])
				sumList.append(areaValue[0])
			else:
				tempList.append(0)

		sumValue = sum(sumList)
		tempList.append(sumValue) 
		trendedDF[sampleName] = tempList

	trendedDF = trendedDF.T
	trendedDF.columns = trendedDF.iloc[0]
	newnew_labels = pd.MultiIndex.from_arrays([reCalcdRTs, meanRRTListforCMPDs, inLineCMPDList], names=['RT', 'RRT', 'Compound'])
	trendedDF = trendedDF.set_axis(newnew_labels, axis=1).iloc[1:]
	trendedDF = trendedDF.groupby(axis=1, level='RRT', group_keys=True).sum()
	print('\n')
	trendedDF = trendedDF.drop('RRT')
	trendedDF = trendedDF.drop('RT')
	trendedDF = trendedDF.drop('Compound')
	combinedRRT =  list(trendedDF.columns)
	floatcomRRT = combinedRRT.copy()
	floatcomRRT.remove('Sum')
	combinedCMPDList = customFunctions.getCMPDListforRRT(floatcomRRT, cmpdKVDict)
	combinedRTs = customFunctions.calRTValues(rtOneAVG, floatcomRRT, 3)
	floatcomRT = combinedRTs.copy()
	combinedCMPDList.append(' ')
	combinedRTs.append('Sum')
	newTopRows = pd.DataFrame()
	newTopRows['RRT'] = combinedRRT
	newTopRows['RT'] = combinedRTs
	newTopRows['Compound'] = combinedCMPDList
	newTopRows = newTopRows.T
	newTopRows.columns = newTopRows.iloc[0]
	trendedDF = pd.concat([newTopRows,trendedDF.loc[:]])
	trendedDF.iloc[0], trendedDF.iloc[1] =  trendedDF.iloc[1].copy(), trendedDF.iloc[0].copy()
	trendedDF = trendedDF.rename(index={'RRT': 'temp'})
	trendedDF = trendedDF.rename(index={'RT': 'RRT'})
	trendedDF = trendedDF.rename(index={'temp': 'RT'})
	print(trendedDF)
	print('\n\n')


	# REBUILD DATAFRAME FOR A PRECISION OF 2 D.P.
	twodpRRTs = []
	for rrt in floatcomRRT:
		twodpRRTs.append(round(rrt,2))
	twodpRTs = []
	for rt in floatcomRT:
		twodpRTs.append(round(float(rt),2))

	statictwodpRRTs = twodpRRTs.copy()
	twodpRRTs.append('Sum')
	twodpRTs.append('Sum')
	twodpTrendedDF = pd.DataFrame(trendedDF.drop('RRT'))
	twodpTrendedDF = twodpTrendedDF.drop('RT')
	twodp_labels = pd.MultiIndex.from_arrays([twodpRTs, twodpRRTs, combinedCMPDList], names=['RT', 'RRT', 'Compound'])
	twodpTrendedDF = twodpTrendedDF.set_axis(twodp_labels, axis=1).iloc[1:]
	twodpTrendedDF = twodpTrendedDF.groupby(axis=1, level='RRT', group_keys=True).sum()
	twodpTopRows = pd.DataFrame()
	twodpcombiRRTs = list(dict.fromkeys(twodpRRTs))
	twodpcombiRTs= customFunctions.calRTValues(rtOneAVG, list(dict.fromkeys(statictwodpRRTs)), 2)
	twodpcombiRTs.append('Sum')
	twodpcombiCMPDList = customFunctions.getCMPDListforRRT(list(dict.fromkeys(statictwodpRRTs)), twodpcmpdKVDict)
	twodpcombiCMPDList.append(' ')
	twodpTopRows['RRT'] = twodpcombiRRTs 
	twodpTopRows['RT'] = twodpcombiRTs
	twodpTopRows['Compound'] = twodpcombiCMPDList
	twodpTopRows = twodpTopRows.T
	twodpTopRows.columns = twodpTopRows.iloc[0]
	#twodpTopRows = twodpTopRows.groupby(axis=1, level='RRT', group_keys=True).sum()
	twodpTrendedDF = pd.concat([twodpTopRows,twodpTrendedDF.loc[:]])
	twodpTrendedDF.iloc[0], twodpTrendedDF.iloc[1] =  twodpTrendedDF.iloc[1].copy(), twodpTrendedDF.iloc[0].copy()
	twodpTrendedDF = twodpTrendedDF.rename(index={'RRT': 'temp'})
	twodpTrendedDF = twodpTrendedDF.rename(index={'RT': 'RRT'})
	twodpTrendedDF = twodpTrendedDF.rename(index={'temp': 'RT'})
	print(twodpTrendedDF)

	
	# CONVERT AREA TO %AREA
	percentAreaDF, prettyperAreaDF = customFunctions.percentAreaCal(trendedDF, newTopRows)
	twodppercentAreaDF, twodpprettyperAreaDF = customFunctions.percentAreaCal(twodpTrendedDF, twodpTopRows)


	# SIMPLIFY UNNAMED IMPURITY PEAKS
	colListList = []
	colLen = int
	for column in twodpprettyperAreaDF.columns:
		colList = twodpprettyperAreaDF[column].tolist()
		colListList += [colList]
		colLen = len(colList)
		#print(colList)

	namelessPeaks = []	
	namedPeaks = []
	for innerlist in colListList:
		if innerlist[2].isspace() or innerlist[2] == '':
			#print(innerlist[1])
			namelessPeaks.append(float(innerlist[1]))
		else:
			namedPeaks.append(float(innerlist[1]))
	
	print('\n\n')
	print(namelessPeaks)
	unminamisedPeaks = namelessPeaks.copy()
	formattedAvgs = []
	for x in range(5):
		namelessPeaks = customFunctions.simplifyRRTs(namelessPeaks)
		formattedAvgs = namelessPeaks


	# REBUILD DATAFRAME FOR SIMPLIFIED DATA
	simpRRTs = namedPeaks.copy() 
	simpRRTs.extend(formattedAvgs)
	simpRRTs.sort()
	simpRTs = customFunctions.calRTValues(rtOneAVG, simpRRTs, 2)
	simpTrendedDF = pd.DataFrame(twodppercentAreaDF)
	simpTrendedDF = simpTrendedDF.drop('RRT')
	simpTrendedDF = simpTrendedDF.drop('RT')
	simp_labels = pd.MultiIndex.from_arrays([simpRTs, simpRRTs, twodpcombiCMPDList[:-1]], names=['RT', 'RRT', 'Compound'])
	simpTrendedDF = simpTrendedDF.set_axis(simp_labels, axis=1).iloc[1:]
	simpTrendedDF = simpTrendedDF.groupby(axis=1, level='RRT', group_keys=True).sum()
	simpTopRows = pd.DataFrame()
	simpcombiRRTs = list(dict.fromkeys(simpRRTs))
	#print(len(simpcombiRRTs))
	simpcombiRTs= customFunctions.calRTValues(rtOneAVG, simpcombiRRTs, 2)
	simpcombiCMPDList = customFunctions.getCMPDListforRRT(simpcombiRRTs, twodpcmpdKVDict)
	simpTopRows['RRT'] = simpcombiRRTs 
	simpTopRows['RT'] = simpcombiRTs
	simpTopRows['Compound'] = simpcombiCMPDList
	simpTopRows = simpTopRows.T
	simpTopRows.columns = simpTopRows.iloc[0]
	#twodpTopRows = twodpTopRows.groupby(axis=1, level='RRT', group_keys=True).sum()
	simpTrendedDF = pd.concat([simpTopRows,simpTrendedDF.loc[:]])
	simpTrendedDF.iloc[0], simpTrendedDF.iloc[1] =  simpTrendedDF.iloc[1].copy(), simpTrendedDF.iloc[0].copy()
	simpTrendedDF = simpTrendedDF.rename(index={'RRT': 'temp'})
	simpTrendedDF = simpTrendedDF.rename(index={'RT': 'RRT'})
	simpTrendedDF = simpTrendedDF.rename(index={'temp': 'RT'})
	simpTrendedDF = simpTrendedDF.replace(0, '-')
	print(simpTrendedDF)

	# GENERATE AND STYLE OUTPUT
	outputName = 'New_output_' + str(file)
	with pd.ExcelWriter(outputName) as writer: 
		twodpprettyperAreaDF.to_excel(writer, sheet_name='2d.p. %area', index=True)
		twodpTrendedDF.to_excel(writer, sheet_name='2d.p. area', index=True)
		prettyperAreaDF.to_excel(writer, sheet_name='3d.p. %area', index=True)
		trendedDF.to_excel(writer, sheet_name='3d.p. area', index=True)
		simpTrendedDF.to_excel(writer, sheet_name='Simple Output', index=True)

	
	StyleTT.StyleTT(outputName)
	print('\n')
	print('Opening Trended Data in Excel, this may take a few moments.')

	
for file in os.listdir(wd):
	#print(file)
	if file.startswith('~$'):
		continue
	elif file.endswith('.xlsx'):
		trendedData = trendHPLC(wd,file)