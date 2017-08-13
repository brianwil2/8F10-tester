### Class for reading in Radiometrics Test Data
#This Module was written on 4/3/2017 
#   Added difference voltage for each cycle
#   Added Reference voltage 4/7/17
#   Added Misc Voltage 4/11/17
#   Added time readin and parcing 7/17/17
# Typical Setup for data taking
# Y0= 'Time' = time since midnight in seconds
# Y1 = Counter = 'Number'
# Y2 = SQRWave = 'SQRwave'
# Y3 = AIN(0) = 'Vnoise'
# Y4 = AIN(1) = 'Vout'
# Y5 = AIN(2) = 'Temp1'
# Y6 = AIN(3) = 'Vref'  Second Channel on OpAmp Chip for Vout
# Y7 = AIN(4) = 'Vmisc' Monitor of Bis voltage with a resistor voltage divider



import numpy
import csv
import time
import copy

#Comverts the strings from the lsit type into float decimal numpy array
def convertStringToFloat(str):
	strNum=numpy.array(str,dtype='S8')
	yStr=strNum.astype(numpy.float64)
	return yStr


def GetRMFile(filename, flag):
    	All_Data=dict()
        data = csv.reader(open(filename, 'rb'), delimiter=",", quotechar='|')
        c0,c1,c2,c3,c4,c5,c6,c7 =[],[],[],[],[],[],[],[]
	for row in data:
		c0.append(row[0])
		c1.append(row[1])
		c2.append(row[2])
		c3.append(row[3])
		c4.append(row[4])
		c5.append(row[5])
		c6.append(row[6])                  
		c7.append(row[7])
		
		
	y0=convertStringToFloat(c0)	
	y1=convertStringToFloat(c1)
	y2=convertStringToFloat(c2)
	y3=convertStringToFloat(c3)
	y4=convertStringToFloat(c4)
	y5=convertStringToFloat(c5)
	y6=convertStringToFloat(c6)
	y7=convertStringToFloat(c7)
	

#This calibrates the temperature sensor between Amps 1 and 2 Equation from Excel
	#tempCal12=152.67*y6[:]-86.62
	tempCal1=((y5[:]-0.805)/0.01)+25
	
	if flag < 1: 
		i=0
		j=0
		vdiff=numpy.zeros(0)
		ymod=y4
		
		while i < len(ymod):
			if (y2[i] == 39):
				j += 1
			i += 1

		for num in range(1,j+1):
		    voff=numpy.mean(ymod[0:20])
		    von=numpy.mean(ymod[20:40])
		    vdiff=numpy.append(vdiff,(voff-von))
		    ymod=ymod[40:]

        if flag >= 1: 
		vdiff= y4 - numpy.mean(y4)
		
		
		
#cut out the time and make it one continuous line won't work with data sets with 2 midnight crossings

 	things=copy.copy(y0[:])
 	
	js=0
	num=0
	i=0
	while js < (len(things)-1):
	    if things[js] > things[js+1]:
		num=js+1
	    js+=1
		
	things[:]-things[num]
	for i in range(num,len(things)):
	    things[i]=things[i]+things[num-1]
	    
	things[:]-things[0]

	All_Data={'Number':y1,
              'SQRwave':y2,
              'Vnoise':y3,
              'Vout':y4,
              'Vdiff':vdiff,
              'Vref':y6,
              'Vmisc':y7,
              'Temp1':y5,
              'Temp1Cal':tempCal1,
              'Time':things
            }
    
	print "Used Current version (7/17/2017 time) of Code with File: " + filename +"  Loaded on: " + time.strftime("%m/%d/%Y") +" at " + time.strftime("%H:%M")+" "+ str(len(y5))+ "  "+str(len(vdiff))
	return All_Data


print "Radiometrics Read File Version 1.53 (7/17/2017) Loaded on " + time.strftime("%m/%d/%Y") +" at " + time.strftime("%H:%M")




