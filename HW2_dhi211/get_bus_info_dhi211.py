#Imports -
from __future__ import print_function
import pandas as pd
import os
import numpy as np
import urllib2
#With line below hashed out, this will run with Python 2
#import urllib.request as urllib2
import sys
import json

#Sys Arg - dictates what can be entered, and whether all information is present. Also stores MTA Key.
if len(sys.argv) != 4:
    print ("You did not enter the appropriate number of arguments. Please try again")
    sys.exit()

mta_key = sys.argv[1]
bus_line = sys.argv[2]
bus_line_csv = sys.argv[3]



#Reading the Data - this sections helps read/process data into a format that can be manipulated.
url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + mta_key + "&VehicleMonitoringDetailLevel=calls&LineRef=" + bus_line
response = urllib2.urlopen(url)
data_rough = response.read()
data = json.loads(data_rough)


#Getting info for each independent bus
indbus = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']


#Creating the Data List using a for loop
datalist = []

for i in indbus:
    dict = {}
    dict['Latitude'] = str(i['MonitoredVehicleJourney']['VehicleLocation']['Latitude'])
    dict['Longitude'] = str(i['MonitoredVehicleJourney']['VehicleLocation']['Longitude'])
    try:
        dict['Stop Name'] = str(i['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['StopPointName'])
    except BaseException:
        dict['Stop Name'] = 'N/A'
    try:
        dict['Stop Status'] = str(i['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['Extensions']['Distances']['PresentableDistance'])
    except BaseException:
        dict['Stop Status'] = 'N/A'
    datalist.append(dict)


df = pd.DataFrame(datalist)

#Converting Dataframe to CSV File
df.to_csv(str(bus_line_csv))
