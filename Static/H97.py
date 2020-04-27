import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

hobo = pd.read_csv('H97_20180907.csv', skiprows=2, usecols=(1, 2, 3, 4),
                   names=['Time', 'T', 'rh', 'Dpt'],
                   parse_dates={'time': [0]},
                   date_parser=lambda x: pd.to_datetime(x).strftime('%m/%d/%y %H:%M:%S'),
                   index_col='time')
hobo = hobo[np.isfinite(hobo["T"])]  # dumps rows with NaNs

# converts filename to Timestamp
fname = "060718_2210_07.csv"
start_time = pd.to_datetime(fname[:-4], format='%d%m%y_%H%M_%S')
utc_time = start_time - pd.Timedelta(hours=3)
print(utc_time)

gps = pd.read_csv(fname, names=['lat', 'lon', 'time'], usecols=[0, 1, 5],
                  index_col='time')

log_time = pd.to_timedelta(gps.index, unit='ms')  # ms to timedelta
gps.index = utc_time + log_time  # adds timedeltas to Timestamp

gps = gps.resample('10s').mean()

gps = gps[~gps.index.duplicated(keep='first')]  # dumps duplicates
hobo = hobo[~hobo.index.duplicated(keep='first')]  # dumps duplicates
##
## creates 10min timeseries
first = gps.iloc[0].name
last = gps.iloc[-1].name

dr = pd.date_range(first, last, freq='10s', name='Time')
hobo = hobo.reindex(dr)
gps = gps.reindex(dr)

df = pd.concat([gps, hobo], axis=1)

x = df['lat'].values
y = df['lon'].values
z = df['T'].values

#plt.plot(df.index, df['T'])
#plt.show()

# df.to_csv('ride1.csv')
plt.figure(figsize=(14, 8))
earth = Basemap(projection='cyl',llcrnrlat=38.18,urcrnrlat=38.30,
                llcrnrlon=21.68, urcrnrlon=21.8, resolution='l', 
                area_thresh=50, lat_0=38, lon_0=21)
earth.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', 
            service='ESRI_Imagery_World_2D', xpixels=720, ypixels=None, 
            dpi=300, verbose=False, )
#earth.bluemarble(alpha=0.42)
earth.drawcoastlines(color='#555566', linewidth=1)
plt.scatter(y, x, z, 
            c=z,alpha=1, zorder=10)
cbar = plt.colorbar()
cbar.set_label('Air Temperature (℃)')
plt.xlabel("2018-07-06, 19:10 to 20:49 UTC")
#plt.savefig('usgs-4.5quakes-bluemarble.png', dpi=350)# -*- coding: utf-8 -*-
#plt.savefig("H97_20180706.png",pad_inches='tight')