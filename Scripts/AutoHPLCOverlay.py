import matplotlib.pyplot as plt
import csv
import os


wd = os.getcwd() + '\\Chromatogram_CSVs\\'
print('Starting Chromatogram Overlay')
print('\n')


def overlayHPLC(chromCSV, j, path):
	i = 0
	RT = []
	RelRes = []
	fullName = path+chromCSV
	#labelName = chromCSV[:-32]
	labelName = chromCSV[:-17]	
	#labelName = chromCSV[:-13]
	if labelName.endswith('_'):
		labelName = labelName[:-1]
	with open (fullName,"r") as csvfile:
		Data = csv.reader(csvfile)
		for row in Data:
			i+=1
			if i > 1:
				RelRes.append(float(row[1])+j)
				RT.append(float(row[0]))
			
	plt.plot(RT,RelRes,label=labelName)



listofCSVs = []
j = 0
for file in os.listdir(wd):
	#print(file)
	if file.endswith('.CSV'):
		j+=3000
		overlayHPLC(file, j, wd)
		listofCSVs.append(file)

lenofList = str(len(listofCSVs))
print('No. of CSVs to overlay: '+lenofList)
hightofoverlay = 3*len(listofCSVs)/10
if hightofoverlay >= 4:
	HoO = hightofoverlay
else:
	HoO = 4
print('Hight of overlay (inches): '+str(HoO))



plt.xlabel('RT / min') 
plt.ylabel('Rel. Response')
plt.legend(fontsize='x-small', reverse=True, bbox_to_anchor=(1, 0.95), frameon=False, labelspacing=1.2)
axes = plt.gca()
#axes.axes.get_yaxis().set_visible(False)
axes.set_yticklabels([])
axes.yaxis.set_tick_params(length=0)
#axes.set_xlim([18,30])
#axes.set_ylim([0,105])
#plt.show()

print('Saving Overlay .png')
print('\n\n')
fig = plt.gcf()
fig.set_size_inches(11, HoO)
fig.savefig("overlayedHPLCtrace.png", bbox_inches = 'tight', dpi=600)

