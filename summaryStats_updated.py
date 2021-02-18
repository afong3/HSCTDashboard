#trying to convert summaryStats to work correctly with the new csv data

import pandas as pd
import numpy as np
import datetime as date
from datetime import datetime
import math

path = "c:/code/python/HSCTDashboard/data/upToData.csv"

#load data into dataframe
data = pd.read_csv(path, header = 0, usecols = ["startTimeLocal", "activityName", "distance", "calories", "movingDuration",
"averageHR", "maxHR", "averageSpeed", "maxSpeed", "elevationGain", "elevationLoss",
"minActivityLapDuration", "lapCount", "type"])
print(data)

#Clean data: Convert to dates, order by dates, reset index
data["startTimeLocal"] = pd.to_datetime(data.startTimeLocal)
data1 = data.sort_values(by = "startTimeLocal").reset_index(drop = True) #drop = True prevents the old index from being added to the dataframe as a column

#Clean data: subsetting the data1 accordingly
cycling_activities = data1.loc[data1["type"] == "Cycling"]
cycling_totalDistance = math.floor(cycling_activities["distance"].sum())
cycling_ElevGain = cycling_activities["elevationGain"].astype("float").sum()
running_activities = data1.loc[data1["type"] == "Running"]
running_totalDistance = math.floor(running_activities["distance"].sum())
running_ElevGain = running_activities["elevationGain"].astype("float").sum()
running_ElevLoss = running_activities["elevationLoss"].astype("float").sum()

##printing for easy reading
print(f'Total Distance Cycled -> {cycling_totalDistance} kilometers')
print(f'Total Cycling Elevation Gain -> {cycling_ElevGain} meteres')
print(f'Total Distance Ran -> {running_totalDistance} kilometers')
print(f'Total Running Elevation Gain -> {running_ElevGain} meteres')
print(f'Total Running Elevation Loss -> {running_ElevLoss} meters')

HSCTDistance = 29
HSCTElevGain = 1830
HSCTElevLoss = 2600

laps_distance = running_totalDistance / HSCTDistance
laps_ElevGain = running_ElevGain / HSCTElevGain
laps_ElevLoss = running_ElevLoss / HSCTElevLoss

print("Laps of HSCT -> " + str(laps_distance))
print("Laps of HSCT Elevation Gain -> " + str(laps_ElevGain))
print("Laps of HSCT Elevation Loss -> " + str(laps_ElevLoss))

##now I want to find how long it took me to do each lap. This should be a stat
##that I try to decrease the time
##Per lap:
##Totals days, total activities, total time running

##When lap_floor[lap_floor == 1] it returns all the activities between 1 and 2
##this means that to calculate the activities for one lap, all you need to do is add
##one value to the total number of activities per lap

cumDist = running_activities["distance"].cumsum()
lap_float = cumDist / HSCTDistance
lap_floor = lap_float.apply(math.floor) #
activities_in_lap = lap_floor[lap_floor == 1].value_counts() + 1 #makes a series so when printing use [1] index
running_dates = running_activities["startTimeLocal"]
#creates lap_count[] list which shows how many activities it took per lap
#right now it looks like it takes me 4 activities to do a distanct lap
lap_count_dist = []
for lap in range(0, math.floor(laps_distance) + 1):
    tempActivities = lap_floor[lap_floor == lap].value_counts() + 1
    ActPerLap = tempActivities.rename("lapCount")
    lap_count_dist.append(ActPerLap)
    print("\n")

#the first value in the series is the current lap, the second value is how long it took to finish that lap
#print(lap_count)

#prints how many activities it took for each lap
for lap in range(0, math.floor(laps_distance)): #uninclusive is alright because this isn't counting the current lap
    print("Activities needed for lap " + str(lap) + " of HSCT Distance: " + str(lap_count_dist[lap][lap])) #[lap][lap] is funky... but pretty sure this is correct to get rid of the series
    print("\n")
#Now I want the amount of days it took per lap

    lap_start_index = lap_floor[lap_floor == 0].index.values[0] #I thought this would be zero, but running is a subset of total activites
    #I could reset the index of the running subset but I like the idea of having the index as the activity number; also this works and I'm lazy
for lap in range(1, math.floor(laps_distance)+1):
     #this calculates the activity number for the first activity during a specific lap
    lap_finish_index = lap_floor[lap_floor == lap].index.values[0]
    date1 = running_dates.loc[lap_start_index].date()
    date2 = running_dates.loc[lap_finish_index].date()
    print("Lap " + str(lap - 1) +" started: " + str(date1)) #lap - 1 is to account for starting with range(1,...)
    print("Lap " + str(lap - 1) +" finished: "  + str(date2))
    days_in_lap = (date2 - date1).days #.days is needed to get ride of the time delta
    print("Days until completion: "  + str(days_in_lap))
    print("\n")
    lap_start_index = lap_finish_index

#Get distance, elevation gain to go
distance_per_complete = laps_distance % 1
elevGain_per_complete = laps_ElevGain % 1
elevLoss_per_complete = laps_ElevLoss % 1

print(distance_per_complete)

distance_left = (1 - distance_per_complete) * HSCTDistance
elevGain_left = (1 - elevGain_per_complete) * HSCTElevGain
elevLoss_left = (1 - elevLoss_per_complete) * HSCTElevLoss

print(f'Distance left: {distance_left} \nElevation Gain Left {elevGain_left} \nElevation Loss Left {elevLoss_left}')

print(distance_per_complete)
