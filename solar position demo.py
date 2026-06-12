import pandas as pd
from pvlib import solarposition
import pytz
from datetime import datetime

#Define location parameters
#For instance, these coordinates correspond to Hiram
LATITUDE = 41.3126
LONGITUDE = -81.1437

#Get the current time within the correct timezone
timezone = pytz.timezone('America/New_York')
currentTime = datetime.now(timezone)

#Format the time with PVLIB
rightTime = pd.DatetimeIndex([currentTime])

#Calculate Sun Position (Zenith and Azimuth)
solpos = solarposition.get_solarposition(rightTime, LATITUDE, LONGITUDE)

#Extract angles
zen = solpos['zenith'].iloc[0]
azi = solpos['azimuth'].iloc[0]
elevation = 90 - zen #How high the sun is in the sky

print(f"Time: {currentTime.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"Azimuth: {azi:.2f}° (Compass direction, 0=North, 90=East)")
print(f"Altitude: {elevation:.2f}° (Height above horizon)")