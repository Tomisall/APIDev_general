import matplotlib.pyplot as plt
import os
import pandas as pd
import plotly.express as px


wd = os.getcwd() + '\\HeatMap_CSVs\\'
print('Starting Heat Map Generation')


def plateUP(path,file):

	fullName = path+file
	sheetDict = {}
	xls = pd.ExcelFile(fullName)
	for sheet in xls.sheet_names[1:]:
		print('\n')
		print(sheet)
		print('\n')
		sheetDict = pd.read_excel(fullName, sheet_name=sheet)
		#print(sheetDict)
		plateSize = len(sheetDict['Name:'].tolist())
		columnList = []
		for sampleName in sheetDict['Name:']:
			sampleName = str(sampleName)
			if sampleName.endswith('A1') or sampleName.endswith('A2') or sampleName.endswith('A3') or sampleName.endswith('A4') or sampleName.endswith('A5') or sampleName.endswith('A6') or sampleName.endswith('A7') or sampleName.endswith('A8') or sampleName.endswith('A9') or sampleName.endswith('A10') or sampleName.endswith('A11') or sampleName.endswith('A12'):
				#yieldPlateA1 = df.loc[(df[sampleName] == 2021) & (df['Month'] == 1), 'Total']
				columnList.append('A')

			elif sampleName.endswith('B1') or sampleName.endswith('B2') or sampleName.endswith('B3') or sampleName.endswith('B4') or sampleName.endswith('B5') or sampleName.endswith('B6') or sampleName.endswith('B7') or sampleName.endswith('B8') or sampleName.endswith('B9') or sampleName.endswith('B10') or sampleName.endswith('B11') or sampleName.endswith('B12'):
				columnList.append('B')

			elif sampleName.endswith('C1') or sampleName.endswith('C2') or sampleName.endswith('C3') or sampleName.endswith('C4') or sampleName.endswith('C5') or sampleName.endswith('C6') or sampleName.endswith('C7') or sampleName.endswith('C8') or sampleName.endswith('C9') or sampleName.endswith('C10') or sampleName.endswith('C11') or sampleName.endswith('C12'):
				columnList.append('C')

			elif sampleName.endswith('D1') or sampleName.endswith('D2') or sampleName.endswith('D3') or sampleName.endswith('D4') or sampleName.endswith('D5') or sampleName.endswith('D6') or sampleName.endswith('D7') or sampleName.endswith('D8') or sampleName.endswith('D9') or sampleName.endswith('D10') or sampleName.endswith('D11') or sampleName.endswith('D12'):
				columnList.append('D')

			elif sampleName.endswith('E1') or sampleName.endswith('E2') or sampleName.endswith('E3') or sampleName.endswith('E4') or sampleName.endswith('E5') or sampleName.endswith('E6') or sampleName.endswith('E7') or sampleName.endswith('E8') or sampleName.endswith('E9') or sampleName.endswith('E10') or sampleName.endswith('E11') or sampleName.endswith('E12'):
				columnList.append('E')

			elif sampleName.endswith('F1') or sampleName.endswith('F2') or sampleName.endswith('F3') or sampleName.endswith('F4') or sampleName.endswith('F5') or sampleName.endswith('F6') or sampleName.endswith('F7') or sampleName.endswith('F8') or sampleName.endswith('F9') or sampleName.endswith('F10') or sampleName.endswith('F11') or sampleName.endswith('F12'):
				columnList.append('F')

			elif sampleName.endswith('G1') or sampleName.endswith('G2') or sampleName.endswith('G3') or sampleName.endswith('G4') or sampleName.endswith('G5') or sampleName.endswith('G6') or sampleName.endswith('G7') or sampleName.endswith('G8') or sampleName.endswith('G9') or sampleName.endswith('G10') or sampleName.endswith('B11') or sampleName.endswith('G12'):
				columnList.append('G')

			else:
				
				columnList.append('z')
		sheetDict['letterRow'] = columnList
		print('\n')
		#print(sheetDict)

		rowList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
		letterList = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
		results = ['Yield', 'Conv']
		
		listAYield = sheetDict.query("letterRow=='A'")["Unnamed: 9"].tolist()
		listBYield = sheetDict.query("letterRow=='B'")["Unnamed: 9"].tolist()
		listCYield = sheetDict.query("letterRow=='C'")["Unnamed: 9"].tolist()
		listDYield = sheetDict.query("letterRow=='D'")["Unnamed: 9"].tolist()
		listEYield = sheetDict.query("letterRow=='E'")["Unnamed: 9"].tolist()
		listFYield = sheetDict.query("letterRow=='F'")["Unnamed: 9"].tolist()
		listGYield = sheetDict.query("letterRow=='G'")["Unnamed: 9"].tolist()

		dictAYield = {}
		dictBYield = {}
		dictCYield = {}
		dictDYield = {}
		dictEYield = {}
		dictFYield = {}
		dictGYield = {}

		listAConv = sheetDict.query("letterRow=='A'")["Unnamed: 8"].tolist()
		listBConv = sheetDict.query("letterRow=='B'")["Unnamed: 8"].tolist()
		listCConv = sheetDict.query("letterRow=='C'")["Unnamed: 8"].tolist()
		listDConv = sheetDict.query("letterRow=='D'")["Unnamed: 8"].tolist()
		listEConv = sheetDict.query("letterRow=='E'")["Unnamed: 8"].tolist()
		listFConv = sheetDict.query("letterRow=='F'")["Unnamed: 8"].tolist()
		listGConv = sheetDict.query("letterRow=='G'")["Unnamed: 8"].tolist()

		dictAConv = {}
		dictBConv = {}
		dictCConv = {}
		dictDConv = {}
		dictEConv = {}
		dictFConv = {}
		dictGConv = {}

		yieldPlate = pd.DataFrame()
		convPlate = pd.DataFrame()

		for result in results:
			if result == 'Yield':
				for letter in letterList:
					if letter == 'A':
						activeList = listAYield
						activeDict = dictAYield
					elif letter == 'B':
						activeList = listBYield
						activeDict = dictBYield
					elif letter == 'C':
						activeList = listCYield
						activeDict = dictCYield
					elif letter == 'D':
						activeList = listDYield
						activeDict = dictDYield
					elif letter == 'E':
						activeList = listEYield
						activeDict = dictEYield
					elif letter == 'F':
						activeList = listFYield
						activeDict = dictFYield
					elif letter == 'G':
						activeList = listGYield
						activeDict = dictGYield
			
					for plateColumn in rowList:
						plateindex = int(plateColumn)-1
						if plateindex < len(activeList):
							#print(plateindex)
							activeDict[rowList[plateindex]] = round(activeList[plateindex],1)
				
						else:	
	
							activeDict[rowList[plateindex]]= '-'
			

					yieldPlate = pd.concat([yieldPlate, pd.DataFrame([activeDict])])

			elif result == 'Conv':
				for letter in letterList:
					if letter == 'A':
						activeList = listAConv
						activeDict = dictAConv
					elif letter == 'B':
						activeList = listBConv
						activeDict = dictBConv
					elif letter == 'C':
						activeList = listCConv
						activeDict = dictCConv
					elif letter == 'D':
						activeList = listDConv
						activeDict = dictDConv
					elif letter == 'E':
						activeList = listEConv
						activeDict = dictEConv
					elif letter == 'F':
						activeList = listFConv
						activeDict = dictFConv
					elif letter == 'G':
						activeList = listGConv
						activeDict = dictGConv
			
					for plateColumn in rowList:
						plateindex = int(plateColumn)-1
						if plateindex < len(activeList):
							#print(plateindex)
							activeDict[rowList[plateindex]] = activeList[plateindex]
				
						else:	

							activeDict[rowList[plateindex]]= '-'
			

					convPlate = pd.concat([convPlate, pd.DataFrame([activeDict])])


		print('Number of Samples: '+str(plateSize))
		if plateSize > 48:
			print('Plate Size: 96-well')
			x=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
			y=['A ', 'B ', 'C ', 'D ', 'E ', 'F ', 'G ']
			print('\n')
			print('Yield Heat Map:')
			print(yieldPlate)
			print('\n')
			print('Conversion Heat Map:')
			print(convPlate)
			print('\n')
		elif plateSize > 24 and plateSize <= 48:
			print('Plate Size: 48-well')
			yieldPlate = yieldPlate.drop(columns=['9','10','11','12'])
			convPlate = convPlate.drop(columns=['9','10','11','12'])
			yieldPlate = yieldPlate.iloc[:-1]
			convPlate = convPlate.iloc[:-1]
			x=['1', '2', '3', '4', '5', '6', '7', '8']
			y=['A ', 'B ', 'C ', 'D ', 'E ', 'F ']
			print('\n')
			print('Yield Heat Map:')
			print(yieldPlate)
			print('\n')
			print('Conversion Heat Map:')
			print(convPlate)
			print('\n')
		else:
			print('Plate Size: 24-well')
			yieldPlate = yieldPlate.drop(columns=['7','8','9','10','11','12'])
			convPlate = convPlate.drop(columns=['7','8','9','10','11','12'])
			yieldPlate = yieldPlate.iloc[:-3]
			convPlate = convPlate.iloc[:-3]
			x=['1', '2', '3', '4', '5', '6']
			y=['A ', 'B ', 'C ', 'D ']
			print('\n')
			print('Yield Heat Map:')
			print(yieldPlate)
			print('\n')
			print('Conversion Heat Map:')
			print(convPlate)
			print('\n')
			
		return(yieldPlate,convPlate,x,y,sheet)


for file in os.listdir(wd):
	#print(file)
	if file.endswith('.xlsx'):
		print(file)
		plateYieldData,plateConvData,xList,yList,sheetName = plateUP(wd,file)
		print('Generating HeatMap Images...')
		yieldFig = px.imshow(plateYieldData,
	        	#labels=dict (y="Factor Settings", color="RRT 0.79 (% area)"), 
	        	labels=dict (color="%th Yield"), 
	        	x=xList,
	        	y=yList,
	        	#color_continuous_scale='Viridis', aspect="auto", text_auto-True, zmin=0, zmax-100) 
	        	#color_continuous_scale='sunsetdark', aspect="auto", text_auto=True, zmin=0, zmax=100) 
	        	#color_continuous_scale='bluyl', aspect="auto", text_auto-True, zmin=0, zmax=100) 
	        	#color_continuous_scale='deep', aspect="auto", text_auto-True, zmin=0, zmax=100)
	        	#color_continuous_scale= 'ylgn', aspect="auto", text_auto=True, zmin=0, zmax=100) 
	        	color_continuous_scale='ylgnbu', aspect="auto", text_auto=True, zmin=0, zmax=100) 

		convFig = px.imshow(plateConvData,
	        	#labels=dict (y="Factor Settings", color="RRT 0.79 (% area)"), 
	        	labels=dict (color="Conversion (% area)"), 
	        	x=xList,
	        	y=yList,
	        	#color_continuous_scale='Viridis', aspect="auto", text_auto-True, zmin=0, zmax-100) 
	        	#color_continuous_scale='sunsetdark', aspect="auto", text_auto=True, zmin=0, zmax=100) 
	        	#color_continuous_scale='bluyl', aspect="auto", text_auto-True, zmin=0, zmax=100) 
	        	#color_continuous_scale='deep', aspect="auto", text_auto-True, zmin=0, zmax=100)
	        	#color_continuous_scale= 'ylgn', aspect="auto", text_auto=True, zmin=0, zmax=100) 
	        	color_continuous_scale='ylgnbu', aspect="auto", text_auto=True, zmin=0, zmax=100) 


		yieldFig.update_layout(
			margin=dict(l=20, r=20, t=20, b=20), 
			height=312, 
			width=500
		)


		#yieldFig.show()
		yieldImageName = str(file)[:-5] + '_' + str(sheetName) + '_Yield_HeatMap.png'
		#yieldFig.write_image("yieldImageName.svg")
		yieldFig.write_image(yieldImageName)
	
		convFig.update_layout(
			margin=dict(l=20, r=20, t=20, b=20), 
			height=312, 
			width=500
		)


		#convFig.show()
		convImageName = str(file)[:-5] + '_' + str(sheetName) + '_Conversion_HeatMap.png'
		#convFig.write_image("convImageName.svg")
		convFig.write_image(convImageName)

print('\n')
exit()
