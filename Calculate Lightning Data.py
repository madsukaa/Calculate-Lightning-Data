import numpy as np
import time
import math
import cmath
from math import atan2
import psutil
import csv
import os
from gpiozero import CPUTemperature
import requests

start = time.time()
fid = open('20181205.txt','r')
fids = np.genfromtxt('20181205.txt', delimiter=',',dtype='f')
times = fids[0:,0]
azimuth = fids[0:,1]
correctedRange = fids[0:,3]
flashtype = fids[0:,4]
polarity = fids[0:,5]

N = len(fid.readlines())
az = []
d = []
ftype = []
pola = []
timeLDloc = []

print ("Program is starting...")

time.sleep(2)

print ("The data is being analyzes...")

for i in range(N):
	if times[i] >= 54000 and times[i] <= 64800:
		az.append(azimuth[i])
		d.append(correctedRange[i])
		ftype.append(flashtype[i])
		pola.append(polarity[i])
		timeLDloc.append(times[i])	

M = len(az)
az2 = []
ranges = []
typeflash = []
polar = []

for i in range(M):
	if d[i] >=1 and d[i]<= 50:
		az2.append(az[i])
		ranges.append(d[i])
		typeflash.append(ftype[i])
		polar.append(pola[i])

C = len(ranges)

print ("Getting coordinates....")
result = CPUTemperature()

if len(ranges) == 0:
	print ('NO FLASHES WITHIN SELECTED RANGE')
else:
        W = len(typeflash)
        flash = []
        flashS = []
        for i in range (W):
                if typeflash[i] == 0:
                        if polar[i] == 0:
                                flash.append(1)
                                flashS.append('CG+')
                        else:
                                flash.append(2)
                                flashS.append('CG-')
                else:
                        if polar[i] == 0:
                                flash.append(3)
                                flashS.append('IC+')
                        else:
                                flash.append(4)
                                flashS.append('IC-')
                                
                                

        
	lat1 = math.radians(2.3139)
	lon1 = math.radians(102.3185)
	
	lat2 = []
	lon2 = []
	rangedeg = []
	
	for i in range(C):
		rangedeg.append(math.radians(ranges[i]/40075.01*360))
	
	for i in range(C):
		dlon2 = math.asin(math.sin(lat1)*math.cos(rangedeg[i]/6378.1)
					+ math.cos(lat1)* math.sin(rangedeg[i])
					* math.cos(az2[i]))
		a = math.sin(az2[i])*math.sin(rangedeg[i]/6378.1)*math.cos(lat1)
		b = math.cos(rangedeg[i]/6378.1) - math.sin(lat1)*math.sin(dlon2)

		dlat2 = lon1 + math.atan2(a, b)
		lat2.append(math.degrees(dlon2))
		lon2.append(math.degrees(dlat2))
	coordinate = []

	f = open('coordinate.txt', 'w')
	fs = open('flash.txt', 'w')
	writeflash = csv.writer(fs, delimiter='\t')
	writeflash.writerows(zip(flash, flashS))
	writer = csv.writer(f, delimiter='\t')
	writer.writerows(zip(lat2, lon2, az2, ranges))
	
	print ("Data has been collected successfully!")
	time.sleep(2)
	f.close()
	print ("Coordinate file and flash file has been created!")

end = time.time()
print ("Temperature %d C" % result.temperature)
print ("Cpu Usage %d " % psutil.cpu_percent())
print ("Time to execute is %d s" % (end-start))
