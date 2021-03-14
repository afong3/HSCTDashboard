#Plots 3D line plot of the HSCT with Lat, Long, Elevation

import gpxpy
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

gpx_file = open('hsct.gpx', 'r')
gpx = gpxpy.parse(gpx_file)


print(len(gpx.tracks))
print(len(gpx.tracks[0].segments))
print(len(gpx.tracks[0].segments[0].points))

data = gpx.tracks[0].segments[0].points

df = pd.DataFrame(columns = ['lon', 'lat', 'ele'])

for point in data:
    df = df.append({'lon': point.longitude,
                    'lat': point.latitude,
                    'ele': point.elevation},
                    ignore_index = True)

fig = plt.figure()
ax = plt.axes(projection = '3d')
ax.set_xlabel  ("Longitude")
ax.set_ylabel  ("Latitude")
ax.set_zlabel  ("Elevation (m)")

#This is an awesome plot because it can show how far I currently am along the HSCT
#It would be cool to have the dot go on the same line but it'd also be cool for it
#to just hover at the same lat long but have the current elevation training sum
ax.plot3D(df['lon'], df['lat'], df['ele'], label = 'Howe Sound Crest Trail')
percentage_distance_completed = 0.206
currentPoint = math.floor(450 - (percentage_distance_completed * 450))
print(currentPoint)
ax.scatter(df.at[currentPoint, 'lon'], df.at[currentPoint, 'lat'], df.at[currentPoint, 'ele'], c = "r")
#for ax.scatter... to get the value, I would use the percentage of var distance
#for example: if I ran 50% of distance of HSCT the value in scatter would be 0.5 * len(data)


plt.show()
